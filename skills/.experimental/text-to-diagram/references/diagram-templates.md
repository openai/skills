# Diagram Templates

Use these templates as a starting point and adapt to the user's content.

## Mermaid Flowchart

```mermaid
flowchart TD
  A[Start] --> B[Step]
  B --> C{Decision?}
  C -->|Yes| D[Branch A]
  C -->|No| E[Branch B]
  D --> F[End]
  E --> F[End]
```

## Mermaid Timeline

```mermaid
timeline
  title "Project Timeline"
  "Phase 1" : "Discovery"
  "Phase 2" : "Build"
  "Phase 3" : "Launch"
```

## Mermaid Sequence Diagram

```mermaid
sequenceDiagram
  participant U as "User"
  participant S as "System"
  participant E as "Email Service"
  U->>S: "Sign Up"
  S->>E: "Send Verification"
  E-->>U: "Verification Email"
  U->>S: "Log In"
```

## Mermaid ER Diagram

```mermaid
erDiagram
  CUSTOMER ||--o{ ORDER : "places"
  ORDER ||--|{ ORDER_ITEM : "contains"
  CUSTOMER {
    string id
    string email
  }
  ORDER {
    string id
    date created_at
  }
  ORDER_ITEM {
    string sku
    int qty
  }
```

## Mermaid Mindmap

```mermaid
mindmap
  root((Topic))
    Branch A
      Subtopic A1
      Subtopic A2
    Branch B
      Subtopic B1
```

## Mermaid C4 (Container)

```mermaid
C4Container
  Person(user, "User")
  System_Boundary(s1, "System") {
    Container(web, "Web App", "React")
    Container(api, "API", "Node")
    ContainerDb(db, "Database", "Postgres")
  }
  Rel(user, web, "Uses")
  Rel(web, api, "Calls")
  Rel(api, db, "Reads/Writes")
```

## Mermaid Class Diagram

```mermaid
classDiagram
  class Order {
    +String id
    +Date createdAt
    +addItem(item)
  }
  class OrderItem {
    +String sku
    +int qty
  }
  Order "1" --> "*" OrderItem
```
