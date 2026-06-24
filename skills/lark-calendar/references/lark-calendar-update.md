# calendar +update

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

更新既有日程字段，或独立增量添加/移除参会人和会议室。

`+update` 支持三类互相独立的动作：更新日程字段、添加参会人/会议室、移除参会人/会议室。它们可以单独执行，也可以在同一次命令中组合执行。

需要的 scopes: ["calendar:calendar.event:update"]

## 推荐命令

```bash
# 更新标题、描述、时间
lark-cli calendar +update \
  --event-id "<EVENT_ID>" \
  --summary "产品评审" \
  --description "评审需求范围、排期与风险" \
  --start "2026-03-12T14:00+08:00" \
  --end "2026-03-12T15:00+08:00"

# 增量添加参会人和会议室
lark-cli calendar +update \
  --event-id "<EVENT_ID>" \
  --add-attendee-ids "ou_aaa,ou_bbb,omm_room"

# 移除参会人和会议室
lark-cli calendar +update \
  --event-id "<EVENT_ID>" \
  --remove-attendee-ids "ou_aaa,omm_room"

# 同时更新日程信息、移除旧会议室、添加新会议室
lark-cli calendar +update \
  --event-id "<EVENT_ID>" \
  --summary "产品评审" \
  --start "2026-03-12T15:00+08:00" \
  --end "2026-03-12T16:00+08:00" \
  --remove-attendee-ids "omm_old_room" \
  --add-attendee-ids "omm_new_room"
```

参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--event-id <id>` | 是 | 要更新的日程 ID。重复性日程要先定位到目标实例的 `event_id`，不要直接使用原重复日程 ID |
| `--calendar-id <id>` | 否 | 日历 ID（省略则使用 `primary`） |
| `--summary <text>` | 否 | 新日程标题。仅在显式传入 `--summary` 时更新；若传空字符串，会把标题清空 |
| `--description <text>` | 否 | 新日程描述。目前 API 方式不支持编辑富文本描述；如果日程描述通过客户端编辑为富文本内容，则使用 API 更新描述会导致富文本格式丢失。仅在显式传入 `--description` 时更新；若传空字符串，会把描述清空 |
| `--start <time>` | 否 | 新开始时间（ISO 8601，如 `2026-03-12T14:00+08:00`）。更新日程时间时必须同时传 `--end` |
| `--end <time>` | 否 | 新结束时间（ISO 8601）。更新日程时间时必须同时传 `--start` |
| `--rrule <rrule>` | 否 | 新重复规则（RFC5545）。**不要使用 COUNT；如需限制次数，推算后转为 UNTIL** |
| `--add-attendee-ids <id_list>` | 否 | 增量添加参会人/会议室，逗号分隔。支持用户 `ou_`、群组 `oc_`、会议室 `omm_` |
| `--remove-attendee-ids <id_list>` | 否 | 增量移除参会人/会议室，逗号分隔。支持用户 `ou_`、群组 `oc_`、会议室 `omm_` |
| `--notify` | 否 | 是否发送更新通知，默认 `true`。可用 `--notify=false` 静默更新 |
| `--dry-run` | 否 | 预览 API 调用，不执行 |

至少需要提供一个动作：`--summary`、`--description`、`--start/--end`、`--rrule`、`--add-attendee-ids` 或 `--remove-attendee-ids`。

## 使用规则

- `--add-attendee-ids` 是**增量添加**，不是替换最终参与人列表。不要用它表达“只保留这些人”。
- 对 `--summary`、`--description`，CLI 以“是否显式传入该 flag”判断是否更新，而不是以“值是否为空”判断；如果显式传入空字符串，会把对应字段清空。
- 只想增删参会人或会议室时，不需要同时传 `--summary`、`--start`、`--end` 等日程字段。
- 只想修改标题、描述、时间或重复规则时，不需要同时传 `--add-attendee-ids` 或 `--remove-attendee-ids`。
- 如需替换某个参与人、群组或会议室，使用 `--remove-attendee-ids <旧ID>` + `--add-attendee-ids <新ID>`。
- 会议室是 resource attendee，必须使用 `omm_` ID 添加到参会人列表，不能脱离日程单独预定。
- 更新重复性日程的某一次实例时，必须先通过 `+agenda`、`events search_event` 或实例视图定位该实例的 `event_id`。
- 如果需要验证更新结果，等待至少 2 秒后再查询，避免同步延迟导致读到旧数据。
- 当同一次命令组合多个动作时，执行顺序为“日程字段 -> 移除参会人 -> 添加参会人”。若中途失败，不会自动回滚已成功步骤；错误信息会说明已完成的步骤。

## 高级用法（完整 API 命令）

`+update` 只覆盖标题、描述、时间、重复规则，以及参会人/会议室的增量添加或移除。

如需更新 `location`（地理位置，不含会议室位置）、`visibility`（日程公开范围）、自定义 `reminders`（提醒设置）、自定义 `attendee_ability`（参与人权限）、自定义 `free_busy_status`（日程忙闲状态）、`color`（颜色）、附件、视频会议信息、全天日程，或在新增参会人时配置可选参加状态 等高级参数，请改用完整的 API 命令。建议先通过 `lark-cli schema calendar.events.patch`、`lark-cli schema calendar.event.attendees.create`、`lark-cli schema calendar.event.attendees.batch_delete` 查看完整参数定义。

> 完整 API 命令的时间参数是 **Unix 秒字符串**（非 ISO 8601）。

## 预约/改约会议室场景

如果用户要“改会议时间”“换会议室”“给现有日程加会议室”，必须先阅读 [`lark-calendar-schedule-meeting.md`](lark-calendar-schedule-meeting.md) 并按其中工作流处理：

- 明确时间且需要会议室：先 `+room-find`，再按需 `+freebusy`，用户确认后再 `+update`。
- 模糊时间或无时间：先 `+suggestion`，如需会议室再批量 `+room-find`，用户确认后再 `+update`。
- 面临时间方案或会议室方案选择时，必须先展示候选方案并等待用户确认。

## 参会人类型

| 前缀 | 类型 | 说明 |
|------|------|------|
| `ou_` | user | 飞书用户 open_id |
| `oc_` | chat | 飞书群组 |
| `omm_` | resource | 会议室 |

> [!CAUTION]
> 这是**写入操作**。执行前必须确认用户意图，特别是移除参会人/会议室或移动会议时间。

## 参考

- [lark-calendar](../SKILL.md) -- 日历全部命令
- [lark-shared](../../lark-shared/SKILL.md) -- 认证和全局参数
- [lark-calendar-schedule-meeting](lark-calendar-schedule-meeting.md) -- 预约/改约会议与会议室工作流
- [lark-calendar-room-find](lark-calendar-room-find.md) -- 查找可用会议室
- [lark-calendar-freebusy](lark-calendar-freebusy.md) -- 查询忙闲
