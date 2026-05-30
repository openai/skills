# Minimal Code Structure

Use this reference when the user asks to scaffold a small FB Ads Manager guard system around Computer Use.

## Layout

```text
fb_ads_guard/
  config.yaml
  main.py
  accounts.py
  operator.py
  reader.py
  recovery.py
  rules.py
  emergency.py
  permissions.py
  audit.py
  models.py
  data/
    latest_ads.csv
  logs/
    audit.jsonl
    screenshots/
```

## Responsibilities

```text
main.py         CLI entrypoint for monitor and shutdown-package commands
accounts.py     Account scope resolution and per-account iteration
operator.py     Computer Use adapter for Ads Manager navigation and pause actions
reader.py       CSV/table reader that returns AdRecord objects
recovery.py     Optional recovery metric normalization and BI merge helpers
rules.py        Routine Ad Set spend guard rules
emergency.py    Package-level and manual shutdown action builders
permissions.py  Action permission checks
audit.py        JSONL audit logging
models.py       Dataclasses and shared type aliases
```

## Models

```python
from dataclasses import dataclass
from typing import Literal, Optional

Level = Literal["campaign", "adset", "ad"]
ActionType = Literal["pause"]


@dataclass
class AdRecord:
    level: Level
    object_id: str
    name: str
    status: str
    spend: float
    results: int
    cpa: Optional[float]
    revenue: Optional[float]
    roas: Optional[float]
    payback: Optional[float]
    package: Optional[str] = None


@dataclass
class Action:
    action: ActionType
    level: Level
    object_id: str
    name: str
    reason: str
    package: Optional[str] = None
    require_confirmation: bool = False


@dataclass
class AdAccount:
    account_id: str
    name: str
    enabled: bool = True
```

## Config

```yaml
mode: read_only

business:
  business_id: "1890587334950745"
  name: "Example BM"

accounts:
  - account_id: act_1304635051001121
    name: "蓝标MADhouse-盛普-2"
    enabled: true

limits:
  max_actions_per_run: 5
  min_spend_to_judge: 20
  cooldown_hours: 6
  max_ads_without_confirmation: 50

rules:
  zero_conversion:
    enabled: true
    spend_multiplier_of_target_cpa: 2
  high_cpa:
    enabled: true
    min_results: 3
    cpa_multiplier: 1.5
  low_recovery:
    enabled: true
    min_spend: 20
    min_roas: 1.0

permissions:
  auto_pause_adset: false
  emergency_pause_ad: false
  emergency_pause_adset: false
  emergency_pause_campaign: false
  auto_resume: false
  auto_increase_budget: false

targets:
  default_target_cpa: 10
  default_min_roas: 1.0

packages:
  com.example.app:
    account_ids:
      - act_xxx
    campaign_name_patterns:
      - com.example.app
    adset_name_patterns:
      - com.example.app
    ad_name_patterns:
      - com.example.app
```

## Rule Engine

```python
from models import Action, AdRecord


def evaluate_adsets(records: list[AdRecord], config: dict) -> list[Action]:
    actions: list[Action] = []
    target_cpa = config["targets"]["default_target_cpa"]
    min_spend = config["limits"]["min_spend_to_judge"]

    for record in records:
        if record.level != "adset":
            continue
        if record.status.lower() != "active":
            continue
        if record.spend < min_spend:
            continue

        zero_cfg = config["rules"]["zero_conversion"]
        if zero_cfg["enabled"]:
            threshold = target_cpa * zero_cfg["spend_multiplier_of_target_cpa"]
            if record.spend > threshold and record.results == 0:
                actions.append(Action(
                    action="pause",
                    level="adset",
                    object_id=record.object_id,
                    name=record.name,
                    reason="zero_conversion_overspend",
                    package=record.package,
                ))
                continue

        high_cpa_cfg = config["rules"]["high_cpa"]
        if high_cpa_cfg["enabled"] and record.cpa is not None:
            if (
                record.results >= high_cpa_cfg["min_results"]
                and record.cpa > target_cpa * high_cpa_cfg["cpa_multiplier"]
            ):
                actions.append(Action(
                    action="pause",
                    level="adset",
                    object_id=record.object_id,
                    name=record.name,
                    reason="high_cpa",
                    package=record.package,
                ))
                continue

        recovery_cfg = config["rules"].get("low_recovery", {})
        if recovery_cfg.get("enabled") and record.roas is not None:
            min_roas = recovery_cfg.get("min_roas", config["targets"].get("default_min_roas", 1.0))
            min_spend_for_recovery = recovery_cfg.get("min_spend", min_spend)
            if record.spend >= min_spend_for_recovery and record.roas < min_roas:
                actions.append(Action(
                    action="pause",
                    level="adset",
                    object_id=record.object_id,
                    name=record.name,
                    reason="low_recovery",
                    package=record.package,
                ))

    return actions
```

## Recovery Metrics

Keep recovery normalization separate from rule evaluation so the rule engine stays simple.

```python
from models import AdRecord


def normalize_recovery(record: AdRecord) -> AdRecord:
    if record.roas is None and record.revenue is not None and record.spend > 0:
        record.roas = record.revenue / record.spend
    if record.payback is None and record.roas is not None:
        record.payback = record.roas
    return record
```

## Account Scope

```python
from models import AdAccount


def configured_accounts(config: dict) -> list[AdAccount]:
    return [
        AdAccount(
            account_id=row["account_id"],
            name=row["name"],
            enabled=row.get("enabled", True),
        )
        for row in config.get("accounts", [])
        if row.get("enabled", True)
    ]


def resolve_accounts(scope: str, config: dict) -> list[AdAccount]:
    accounts = configured_accounts(config)
    if scope == "current":
        return accounts[:1]
    if scope == "all":
        return accounts
    raise ValueError(f"Unknown account scope: {scope}")
```

## Emergency Package Shutdown

```python
from models import Action, AdRecord


def build_package_shutdown_actions(
    package: str,
    records: list[AdRecord],
    config: dict,
) -> list[Action]:
    if package not in config["packages"]:
        raise ValueError(f"Unknown package: {package}")

    actions: list[Action] = []

    for record in records:
        if record.status.lower() != "active":
            continue
        if record.package != package and package not in record.name:
            continue

        actions.append(Action(
            action="pause",
            level=record.level,
            object_id=record.object_id,
            name=record.name,
            reason="package_emergency_shutdown",
            package=package,
            require_confirmation=(record.level == "campaign"),
        ))

    return actions
```

## Permissions

```python
from models import Action


def allowed(action: Action, config: dict) -> bool:
    permissions = config["permissions"]
    if config.get("mode") == "read_only":
        return False

    if action.level == "adset":
        if action.reason == "package_emergency_shutdown":
            return bool(permissions.get("emergency_pause_adset"))
        return bool(permissions.get("auto_pause_adset"))

    if action.level == "ad":
        return bool(permissions.get("emergency_pause_ad"))

    if action.level == "campaign":
        return bool(permissions.get("emergency_pause_campaign"))

    return False
```

## Operator Interface

Keep Computer Use code behind this interface so business rules can be tested without a browser.

```python
from models import Action


class AdsManagerOperator:
    def open_ads_manager(self) -> None:
        pass

    def switch_account(self, account: str) -> None:
        pass

    def switch_level(self, level: str) -> None:
        pass

    def search_object(self, object_id: str, name: str) -> None:
        pass

    def screenshot(self, label: str) -> str:
        pass

    def pause(self, action: Action) -> bool:
        self.switch_level(action.level)
        self.search_object(action.object_id, action.name)
        before = self.screenshot(f"before_{action.object_id}")

        # Computer Use implementation:
        # 1. verify exactly one matching result
        # 2. verify exact name or ID
        # 3. verify current status is Active
        # 4. click delivery toggle
        # 5. wait for Paused/Off status

        after = self.screenshot(f"after_{action.object_id}")
        return bool(before and after)
```

## Reader And Audit

```python
import csv
import json
from datetime import datetime
from models import AdRecord


def load_records(path: str) -> list[AdRecord]:
    records: list[AdRecord] = []
    with open(path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            records.append(AdRecord(
                level=row["level"],
                object_id=row["object_id"],
                name=row["name"],
                status=row["status"],
                spend=float(row["spend"] or 0),
                results=int(row["results"] or 0),
                cpa=float(row["cpa"]) if row.get("cpa") else None,
                revenue=float(row["revenue"]) if row.get("revenue") else None,
                roas=float(row["roas"]) if row.get("roas") else None,
                payback=float(row["payback"]) if row.get("payback") else None,
                package=row.get("package") or None,
            ))
    return records


def log_event(path: str, payload: dict) -> None:
    payload["time"] = datetime.now().isoformat(timespec="seconds")
    with open(path, "a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False) + "\n")
```

## CLI Flow

```python
import argparse
import yaml
from audit import log_event
from emergency import build_package_shutdown_actions
from operator import AdsManagerOperator
from permissions import allowed
from reader import load_records
from rules import evaluate_adsets


def execute_actions(actions, config):
    operator = AdsManagerOperator()
    operator.open_ads_manager()
    executed = 0

    for action in actions:
        if executed >= config["limits"]["max_actions_per_run"]:
            break
        if action.require_confirmation:
            log_event("logs/audit.jsonl", {
                "result": "skipped_confirmation_required",
                "action": action.__dict__,
            })
            continue
        if not allowed(action, config):
            log_event("logs/audit.jsonl", {
                "result": "skipped_permission_denied",
                "action": action.__dict__,
            })
            continue

        success = operator.pause(action)
        log_event("logs/audit.jsonl", {
            "result": "success" if success else "failed",
            "action": action.__dict__,
        })
        executed += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["monitor", "shutdown-package"])
    parser.add_argument("--scope", choices=["current", "all"], default="current")
    parser.add_argument("--package")
    args = parser.parse_args()

    with open("config.yaml", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if args.command == "monitor":
        for account in resolve_accounts(args.scope, config):
            # In production, switch the UI/export path per account before reading.
            records = load_records(f"data/{account.account_id}_latest_ads.csv")
            execute_actions(evaluate_adsets(records, config), config)
    elif args.command == "shutdown-package":
        if not args.package:
            raise ValueError("--package is required")
        package_cfg = config["packages"][args.package]
        for account_id in package_cfg.get("account_ids", []):
            records = load_records(f"data/{account_id}_latest_ads.csv")
            actions = build_package_shutdown_actions(args.package, records, config)
            execute_actions(actions, config)


if __name__ == "__main__":
    main()
```

## CSV Fixture

```csv
level,object_id,name,status,spend,results,cpa,revenue,roas,payback,package
adset,238001,US_Android_com.example.app_PURCHASE,active,35,0,,0,0,0,com.example.app
ad,238002,US_Android_com.example.app_PURCHASE_Video01,active,12,0,,0,0,0,com.example.app
campaign,238003,com.example.app_MAIN,active,300,10,30,360,1.2,1.2,com.example.app
```
