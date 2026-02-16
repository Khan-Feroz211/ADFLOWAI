# 📊 ADFLOWAI - Visual Architecture Diagrams

This file contains Mermaid diagrams that can be rendered in GitHub, VS Code (with extension), or any Mermaid-compatible viewer.

---

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web Browser]
        B[Mobile App]
        C[API Client]
    end
    
    subgraph "API Gateway"
        D[Nginx/Load Balancer]
    end
    
    subgraph "Application Layer"
        E[Flask API Server]
        F[Campaign Manager]
        G[AI Optimization Engine]
    end
    
    subgraph "Data Layer"
        H[(PostgreSQL Database)]
        I[(Redis Cache)]
    end
    
    subgraph "Background Tasks"
        J[Celery Worker]
        K[Celery Beat]
    end
    
    subgraph "Platform Integrations"
        L[Google Ads API]
        M[Facebook Ads API]
        N[LinkedIn Ads API]
        O[Instagram Ads API]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    E --> F
    E --> G
    F --> H
    F --> I
    G --> H
    G --> I
    J --> F
    K --> J
    F --> L
    F --> M
    F --> N
    F --> O
```

---

## 🔄 Campaign Creation Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant CampaignManager
    participant AI
    participant Database
    participant PlatformAPI

    User->>Frontend: Create Campaign
    Frontend->>API: POST /api/v1/campaigns
    API->>CampaignManager: create_campaign()
    CampaignManager->>Database: Save Campaign
    CampaignManager->>AI: Initialize Performance Score
    AI-->>CampaignManager: Score: 0.5
    CampaignManager->>Database: Create Platform Campaigns
    Database-->>CampaignManager: Campaign Created
    CampaignManager->>PlatformAPI: Deploy to Platforms
    PlatformAPI-->>CampaignManager: Platform IDs
    CampaignManager-->>API: Campaign Object
    API-->>Frontend: Success Response
    Frontend-->>User: Show Campaign Dashboard
```

---

## 🤖 AI Optimization Flow

```mermaid
flowchart TD
    A[Start: Scheduled/Manual Trigger] --> B[Fetch Campaign Data]
    B --> C[Fetch Historical Metrics]
    C --> D[Fetch Platform Performance]
    D --> E{Sufficient Data?}
    E -->|No| F[Use Rule-Based Logic]
    E -->|Yes| G[Extract ML Features]
    G --> H[Run ML Models]
    H --> I[Performance Prediction]
    H --> J[Budget Optimization]
    H --> K[Anomaly Detection]
    I --> L{Performance Score}
    L -->|< 0.3| M[Recommend: PAUSE]
    L -->|0.3-0.7| N[Recommend: MAINTAIN]
    L -->|> 0.8| O[Recommend: INCREASE BUDGET]
    J --> P[Calculate Optimal Allocation]
    K --> Q{Anomaly Detected?}
    Q -->|Yes| R[Send Alert]
    Q -->|No| S[Continue]
    M --> T[Execute Recommendations]
    N --> T
    O --> T
    P --> T
    R --> T
    S --> T
    T --> U[Update Database]
    U --> V[Log Optimization]
    V --> W[Send Notifications]
    W --> X[End]
```

---

## 🗄️ Database Schema

```mermaid
erDiagram
    USERS ||--o{ CAMPAIGNS : creates
    USERS ||--o{ API_KEYS : owns
    CAMPAIGNS ||--o{ PLATFORM_CAMPAIGNS : "has many"
    CAMPAIGNS ||--o{ METRICS_HISTORY : tracks
    CAMPAIGNS ||--o{ OPTIMIZATION_LOGS : "has logs"
    
    USERS {
        int id PK
        string username
        string email
        string password_hash
        string company
        string role
        boolean is_active
        timestamp created_at
    }
    
    CAMPAIGNS {
        int id PK
        int user_id FK
        string name
        float total_budget
        float spent_budget
        string status
        json target_audience
        timestamp start_date
        timestamp end_date
        float performance_score
        int impressions
        int clicks
        int conversions
    }
    
    PLATFORM_CAMPAIGNS {
        int id PK
        int campaign_id FK
        string platform
        string platform_campaign_id
        float allocated_budget
        float spent_budget
        float performance_score
        boolean is_active
    }
    
    METRICS_HISTORY {
        int id PK
        int campaign_id FK
        string platform
        timestamp recorded_at
        int impressions
        int clicks
        int conversions
        float spent
        float performance_score
    }
    
    OPTIMIZATION_LOGS {
        int id PK
        int campaign_id FK
        string action
        string reason
        json before_state
        json after_state
        float confidence_score
        boolean success
        timestamp performed_at
    }
    
    API_KEYS {
        int id PK
        int user_id FK
        string key
        string name
        boolean is_active
        timestamp created_at
        timestamp expires_at
    }
```

---

## 🚀 Deployment Flow

```mermaid
flowchart LR
    A[GitHub Push] --> B[GitHub Actions]
    B --> C{Tests Pass?}
    C -->|No| D[Notify Developer]
    C -->|Yes| E[Build Docker Image]
    E --> F[Push to Registry]
    F --> G{Environment}
    G -->|Dev| H[Deploy to Dev]
    G -->|Staging| I[Deploy to Staging]
    G -->|Prod| J{Approval?}
    J -->|Yes| K[Deploy to Production]
    J -->|No| L[Stop]
    K --> M[Health Check]
    M --> N{Healthy?}
    N -->|Yes| O[Success!]
    N -->|No| P[Rollback]
```

---

## 🔐 Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant JWT
    participant Database

    User->>Frontend: Enter Credentials
    Frontend->>API: POST /api/v1/auth/login
    API->>Database: Verify User
    Database-->>API: User Found
    API->>JWT: Generate Token
    JWT-->>API: Access + Refresh Tokens
    API-->>Frontend: Return Tokens
    Frontend->>Frontend: Store Tokens
    Frontend->>API: API Request + Token
    API->>JWT: Verify Token
    JWT-->>API: Token Valid
    API-->>Frontend: Return Data
```

---

## 📊 Data Flow - Metrics Update

```mermaid
graph LR
    A[Platform APIs] -->|Pull Metrics| B[Integration Layer]
    B -->|Raw Data| C[Data Processor]
    C -->|Normalized| D[Campaign Manager]
    D -->|Save| E[(Database)]
    D -->|Cache| F[(Redis)]
    D -->|Trigger| G[AI Engine]
    G -->|Analysis| H[Optimization Service]
    H -->|Updates| D
    D -->|Notification| I[Alert Service]
    I -->|Email/Slack| J[User]
```

---

## 🎯 Performance Optimization Decision Tree

```mermaid
flowchart TD
    A[Campaign Performance Check] --> B{Performance Score}
    B -->|< 0.3| C[Low Performance]
    B -->|0.3-0.5| D[Below Average]
    B -->|0.5-0.8| E[Good Performance]
    B -->|> 0.8| F[Excellent Performance]
    
    C --> G{Spent > 50%?}
    G -->|Yes| H[PAUSE Campaign]
    G -->|No| I[Monitor Closely]
    
    D --> J{Trend}
    J -->|Declining| K[Decrease Budget 30%]
    J -->|Stable| L[Maintain]
    J -->|Improving| M[Monitor]
    
    E --> N{Budget Remaining}
    N -->|< 20%| O[Maintain]
    N -->|> 20%| P[Slight Increase 10%]
    
    F --> Q{Budget Remaining}
    Q -->|< 20%| R[Request More Budget]
    Q -->|> 20%| S[Increase Budget 50%]
    
    H --> T[Log Action]
    K --> T
    L --> T
    P --> T
    S --> T
    T --> U[Notify User]
```

---

## 🏢 Multi-Tenant Architecture

```mermaid
graph TB
    subgraph "Organization A"
        A1[User 1] --> A2[Campaigns]
        A3[User 2] --> A2
        A2 --> A4[Data Isolation]
    end
    
    subgraph "Organization B"
        B1[User 3] --> B2[Campaigns]
        B3[User 4] --> B2
        B2 --> B4[Data Isolation]
    end
    
    subgraph "Shared Services"
        C1[Authentication]
        C2[ML Models]
        C3[Platform APIs]
    end
    
    A4 --> C1
    A4 --> C2
    A4 --> C3
    B4 --> C1
    B4 --> C2
    B4 --> C3
    
    C2 --> D[(Shared ML Models)]
    C3 --> E[External Platforms]
```

---

## 📈 Scaling Strategy

```mermaid
graph TB
    A[Load Balancer] --> B[API Server 1]
    A --> C[API Server 2]
    A --> D[API Server 3]
    
    B --> E[(Read Replica 1)]
    C --> E
    D --> E
    
    B --> F[(Master DB)]
    C --> F
    D --> F
    
    F --> G[(Read Replica 2)]
    
    B --> H[Redis Cluster]
    C --> H
    D --> H
    
    I[Celery Worker Pool] --> F
    I --> H
    
    J[ML Model Server] --> K[(Model Cache)]
    B --> J
    C --> J
    D --> J
```

---

## 🔄 CI/CD Pipeline Visualization

```mermaid
graph LR
    A[Code Commit] --> B[GitHub Actions]
    B --> C[Lint & Format]
    B --> D[Type Check]
    B --> E[Unit Tests]
    B --> F[Integration Tests]
    
    C --> G{All Checks Pass?}
    D --> G
    E --> G
    F --> G
    
    G -->|No| H[Notify Developer]
    G -->|Yes| I[Build Docker]
    
    I --> J[Security Scan]
    J --> K[Push to Registry]
    
    K --> L{Branch?}
    L -->|develop| M[Deploy Dev]
    L -->|staging| N[Deploy Staging]
    L -->|main| O{Manual Approve?}
    
    O -->|Yes| P[Deploy Production]
    O -->|No| Q[Stop]
    
    P --> R[Health Check]
    R --> S{Healthy?}
    S -->|Yes| T[Success]
    S -->|No| U[Auto Rollback]
```

---

## 🎯 How to Use These Diagrams

### In VS Code:
1. Install "Markdown Preview Mermaid Support" extension
2. Open this file in VS Code
3. Use Preview (Ctrl+Shift+V)

### In GitHub:
- These diagrams render automatically in README or documentation files

### Online Editor:
- Visit: https://mermaid.live/
- Paste any diagram code to visualize and edit

---

**These diagrams provide a complete visual understanding of ADFLOWAI's architecture!**
