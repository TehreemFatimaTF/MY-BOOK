---
id: 3
title: "Physical AI Spec Update"
stage: spec
date_iso: "2025-12-14"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "physical-ai-textbook"
branch: "1-physical-ai-textbook"
user: "user"
command: "/sp.specify"
labels:
  - "specification"
  - "textbook"
  - "robotics"
  - "physical-ai"
  - "update"
links:
  spec: "specs/1-physical-ai-textbook/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/1-physical-ai-textbook/spec.md"
tests_yaml: []
---

# Physical AI & Humanoid Robotics – Specification Update

## PROMPT_TEXT

Physical AI & Humanoid Robotics – AI-Native Textbook Platform

This project consists of a Docusaurus-based textbook frontend and a Python backend implementing a RAG chatbot and personalization features.

--------------------------------------------------
SPEC 1: FRONTEND (TEXTBOOK + UI)
--------------------------------------------------

Frontend Stack:
- Docusaurus
- React (Docusaurus pages)
- GitHub Pages deployment
- MCP Context7 (Docusaurus documentation)
- MCP GitHub (deployment automation)

Book Structure (docs/):
The Course Details
2
Physical AI & Humanoid Robotics
Focus and Theme: AI Systems in the Physical World. Embodied Intelligence.
Goal: Bridging the gap between the digital brain and the physical body. Students
apply their AI knowledge to control Humanoid Robots in simulated and real-world
environments.
Quarter Overview
The future of AI extends beyond digital spaces into the physical world. This capstone
quarter introduces Physical AI—AI systems that function in reality and comprehend
physical laws. Students learn to design, simulate, and deploy humanoid robots
capable of natural human interactions using ROS 2, Gazebo, and NVIDIA Isaac.
● Module 1: The Robotic Nervous System (ROS 2)
○ Focus: Middleware for robot control.
○ ROS 2 Nodes, Topics, and Services.
○ Bridging Python Agents to ROS controllers using rclpy.
○ Understanding URDF (Unified Robot Description Format) for
humanoids.
● Module 2: The Digital Twin (Gazebo & Unity)
○ Focus: Physics simulation and environment building.
○ Simulating physics, gravity, and collisions in Gazebo.
○ High-fidelity rendering and human-robot interaction in Unity.
○ Simulating sensors: LiDAR, Depth Cameras, and IMUs.
● Module 3: The AI-Robot Brain (NVIDIA Isaac™)
○ Focus: Advanced perception and training.
○ NVIDIA Isaac Sim: Photorealistic simulation and synthetic data
generation.
○ Isaac ROS: Hardware-accelerated VSLAM (Visual SLAM) and
navigation.
○ Nav2: Path planning for bipedal humanoid movement.
● Module 4: Vision-Language-Action (VLA)
○ Focus: The convergence of LLMs and Robotics.
○ Voice-to-Action: Using OpenAI Whisper for voice commands.
○ Cognitive Planning: Using LLMs to translate natural language ("Clean
the room") into a sequence of ROS 2 actions.
○ Capstone Project: The Autonomous Humanoid. A final project where a
simulated robot receives a voice command, plans a path, navigates
obstacles, identifies an object using computer vision, and manipulates
it.
Why Physical AI Matters
Humanoid robots are -based instances (like AWS RoboMaker or NVIDIA's
cloud delivery for Omniverse), though this introduces significant latency and cost
complexity.
Building a "Physical AI" lab is a significant investment. You will have to choose
between building a physical On-Premise Lab at Home (High CapEx) versus running
a Cloud-Native Lab (High OpEx).
Option 2 High OpEx: The "Ether" Lab (Cloud-Native)
Best for: Rapid deployment, or students with weak laptops.
1. Cloud Workstations (AWS/Azure) Instead of buying PCs, you rent instances.
● Instance Type: AWS g5.2xlarge (A10G GPU, 24GB VRAM) or g6e.xlarge.
● Software: NVIDIA Isaac Sim on Omniverse Cloud (requires specific AMI).
● Cost Calculation:
○ Instance cost: ~$1.50/hour (spot/on-demand mix).
○ Usage: 10 hours/week × 12 weeks = 120 hours.
○ Storage (EBS volumes for saving environments): ~$25/quarter.
○ Total Cloud Bill: ~$205 per quarter.
2. Local "Bridge" Hardware You cannot eliminate hardware entirely for "Physical
AI." You still need the edge devices to deploy the code physically.
● Edge AI Kits: You still need the Jetson Kit for the physical deployment phase.
○ Cost: $700 (One-time purchase).
● Robot: You still need one physical robot for the final demo.
○ Cost: $3,000 (Unitree Go2 Standard).
The Economy Jetson Student Kit
Best for: Learning ROS 2, Basic Computer Vision, and Sim-to-Real control.
Component Model Price
(Approx.)
Notes
The Brain NVIDIA Jetson
Orin Nano Super
Dev Kit (8GB)
$249 New official MSRP (Price
dropped from ~$499).
Capable of 40 TOPS.
The Eyes Intel RealSense
D435i
$349 Includes IMU (essential for
SLAM). Do not buy the D435
(non-i).
The Ears ReSpeaker USB
Mic Array v2.0
$69 Far-field microphone for voice
commands (Module 4).
Wi-Fi (Included in Dev
Kit)
$0 The new "Super" kit includes
the Wi-Fi module
pre-installed.
Power/Misc SD Card (128GB)
+ Jumper Wires
$30 High-endurance microSD
card required for the OS.
8
TOTAL
3. The Latency Trap (Hidden Cost)
~$700 per
kit
● Simulating in the cloud works well, but controlling a real robot from a cloud
instance is dangerous due to latency.
● Solution: Students train in the Cloud, download the model (weights), and flash
it to the local Jetson kit

Landing Pages:
1. Home Page (Hero + CTA)
2. Why Choose This Book?
3. Modules Page (Card-based UI → click opens chapters)
4. Ready to Build the Future?

Per Chapter UI:
- "Translate to Urdu" button
- "Personalize Content" button (visible when logged in)

--------------------------------------------------
SPEC 2: BACKEND (RAG + AUTH + PERSONALIZATION)
--------------------------------------------------

Backend Folder Rules:
- Backend folder must be reviewed first.
- Existing files must NOT be rewritten.
- Minimal files only.
- Every file must include comments explaining purpose.

Current Backend Status (Already Implemented):
- Sitemap-based ingestion
- Text extraction (trafilatura)
- Chunking
- Cohere Embed v3 embeddings
- Qdrant Cloud storage
- RAG retrieval
- OpenAI Agents SDK
- Tool-based retrieval
- Book-only answering
- Local backend running

Backend Stack:
- Python
- FastAPI
- Qdrant Cloud
- Cohere
- OpenAI Agents SDK
- Better-auth (signup/signin)
- Neon Serverless Postgres

Backend Responsibilities:
- Serve chatbot API
- Authenticate users
- Store user background (software/hardware)
- Personalize responses based on user profile
- Translate chapter content to Urdu on demand
- Restrict chatbot answers to textbook content only

--------------------------------------------------
SPEC 3: FRONTEND ↔ BACKEND CONNECTION
--------------------------------------------------

Connection Rules:
- Frontend communicates via REST APIs
- Authentication tokens handled securely
- Logged-in users get personalized responses
- Chapter page buttons trigger backend APIs
- Chat widget embedded inside the book UI

--------------------------------------------------
SPEC 4: BONUS & FINALIZATION
--------------------------------------------------

Bonus Features:
- Claude Code Subagents
- Agent Skills reusable across chapters
- User-based content personalization
- Urdu translation
- Clean GitHub deployment
- Scoring optimization (max points)

Non-Functional Requirements:
- Clean architecture
- Minimal files
- Clear comments
- Production-ready code
- Deterministic workflows

Definition of Success:
- Book deployed
- Backend connected
- Chatbot works
- Personalization works
- Translation works
- Repo published

## RESPONSE_TEXT

Successfully updated the feature specification for the Physical AI & Humanoid Robotics textbook platform to include the detailed course content and requirements. The updated specification now includes:

- Comprehensive user stories for all 4 modules (ROS 2, Digital Twin, NVIDIA Isaac, VLA)
- Detailed functional requirements covering the Physical AI curriculum
- Enhanced key entities including hardware profiles and capstone projects
- Success criteria specific to Physical AI learning outcomes
- Edge cases specific to robotics education

The specification maintains all original requirements while adding the detailed Physical AI course content including modules on robotic nervous systems, digital twins, AI-robot brains, and vision-language-action systems.

## OUTCOME

Specification updated successfully at specs/1-physical-ai-textbook/spec.md with detailed Physical AI curriculum content.

## EVALUATION

The updated specification now fully captures the Physical AI & Humanoid Robotics course requirements with specific content on ROS 2, simulation, NVIDIA Isaac, and VLA systems, while maintaining all original platform requirements.