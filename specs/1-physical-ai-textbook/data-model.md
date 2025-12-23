# Data Model: Physical AI & Humanoid Robotics Textbook

## Entity: User
**Description**: Represents a registered learner with hardware/software background information, authentication credentials, and personalized preferences

**Fields**:
- `id` (UUID, primary key): Unique identifier for the user
- `email` (string, required): User's email address for authentication
- `name` (string, required): User's display name
- `created_at` (timestamp): Account creation date
- `updated_at` (timestamp): Last update to user profile
- `hardware_background` (JSON): User's hardware experience (e.g., {"ros_experience": "beginner", "nvidia_hardware": ["jetson", "orin"]})
- `software_background` (JSON): User's software experience (e.g., {"programming_languages": ["python", "c++"], "robotics_frameworks": ["ros2", "isaac"]})
- `preferred_language` (string): User's preferred language (default: "en")
- `personalization_enabled` (boolean): Whether personalization features are enabled

**Validation Rules**:
- Email must be valid email format
- Name must be 1-100 characters
- hardware_background and software_background must follow predefined schema

## Entity: TextbookContent
**Description**: Represents the structured educational material organized in modules, chapters, and sections with metadata for personalization

**Fields**:
- `id` (UUID, primary key): Unique identifier for the content
- `title` (string, required): Title of the chapter/module
- `slug` (string, required, unique): URL-friendly identifier
- `content_type` (enum: "module", "chapter", "section"): Type of content
- `module_number` (integer): Module number (e.g., 1 for "Module 1: ROS 2")
- `chapter_number` (integer): Chapter number within module
- `content_en` (text, required): English content in markdown format
- `content_ur` (text): Urdu translation of content
- `metadata` (JSON): Additional metadata for personalization (e.g., {"target_hardware": ["ros", "nvidia"], "difficulty": "intermediate"})
- `parent_id` (UUID, foreign key): Reference to parent module/chapter (null for root modules)
- `order_index` (integer): Order of content within parent
- `created_at` (timestamp): Creation date
- `updated_at` (timestamp): Last update

**Validation Rules**:
- Slug must be unique across all content
- Module numbers must be positive integers
- Content must be in valid markdown format
- Parent-child relationships must form a valid tree structure

## Entity: ChatSession
**Description**: Represents a user's interaction session with the AI assistant

**Fields**:
- `id` (UUID, primary key): Unique identifier for the session
- `user_id` (UUID, foreign key): Reference to the user
- `created_at` (timestamp): Session start time
- `updated_at` (timestamp): Last activity in session
- `title` (string): Session title (auto-generated from first query)

**Validation Rules**:
- User ID must reference an existing user
- Session must be associated with an authenticated user

## Entity: ChatMessage
**Description**: Represents an individual message in a chat session

**Fields**:
- `id` (UUID, primary key): Unique identifier for the message
- `session_id` (UUID, foreign key): Reference to the chat session
- `sender` (enum: "user", "assistant"): Who sent the message
- `content` (text, required): The message content
- `timestamp` (timestamp): When the message was sent
- `relevant_content_ids` (JSON): IDs of textbook content referenced in the response

**Validation Rules**:
- Session ID must reference an existing session
- Sender must be either "user" or "assistant"
- Content must not exceed 10,000 characters

## Entity: TranslationCache
**Description**: Caches translated content to improve performance

**Fields**:
- `id` (UUID, primary key): Unique identifier
- `content_id` (UUID, foreign key): Reference to original content
- `target_language` (string, required): Target language code (e.g., "ur")
- `translated_content` (text, required): Cached translated content
- `created_at` (timestamp): Cache creation time
- `updated_at` (timestamp): Last cache update
- `expires_at` (timestamp): When cache entry expires

**Validation Rules**:
- Content ID must reference an existing textbook content
- Target language must be a supported language code
- Cache entries should expire after 24 hours

## Relationships:

1. **User → ChatSession**: One-to-many (one user can have multiple chat sessions)
2. **ChatSession → ChatMessage**: One-to-many (one session contains multiple messages)
3. **TextbookContent → TextbookContent**: Self-referencing parent-child (modules contain chapters, chapters contain sections)
4. **ChatMessage → TextbookContent**: Many-to-many (messages can reference multiple content pieces)
5. **TextbookContent → TranslationCache**: One-to-many (content can have multiple cached translations)

## State Transitions:

### User Profile:
- New registration → Profile created with basic info
- Profile completion → Background info added
- Language preference → Preferred language updated

### Content Access:
- Unauthenticated → Access to public content only
- Authenticated → Access to personalized content
- Session active → Chat history maintained