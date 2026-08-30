# Architectural Standards & Best Practices

## Core Architectural Principles

- **Modularity & Decoupling**: Keep application and domain logic modular and decoupled from transport/framework-specific handlers where practical.
- **Explicit Interfaces**: Use explicit types, data transfer objects, and clear interface contracts across module boundaries.
- **Database Timestamp Rules**: Always include `created_at` and `modified_at` timestamp columns on all database models, entity tables, and persistence schemas.
