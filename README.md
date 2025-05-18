# sturdy-disco

# Sphere-Based Civilization Game

A prototype civilization simulation game rendered on a spherical world, built with modern OpenGL using Python.

This project aims to create a 3D spherical world for strategy and civilization gameplay, using OpenGL for rendering and GLFW for window and input management. The current implementation provides the foundation for rendering on a sphere and includes modular components like window management and shader handling.

---

## 🌍 Current State

### ✅ Core Features Implemented:
- **Window Management**:  
  - Fullscreen OpenGL context setup using GLFW.  
  - Graceful shutdown via ESC key.
  - Modular class-based structure (`Window` class).

- **Shader System**:  
  - Class-based shader manager (`Shader`) for compiling and linking vertex and fragment shaders.  
  - Support for dynamic uniform updates.

- **Rendering Foundation**:  
  - Basic OpenGL clear loop with customizable background color.  
  - Ready for integration of VBOs, VAOs, and 3D geometry (e.g., spheres).

---

## 🧰 Dependencies

### Required:
```bash
pip install glfw PyOpenGL

 Project Structure

 sturdy-disco/
├── main.py              # Entry point: creates Window instance and runs the app
├── window.py            # Contains Window class for managing GLFW and main loop
├── shader.py            # Shader class for loading/compiling GLSL shaders
└── shaders/             # Folder for GLSL shader source files
    ├── simple_vertex.glsl
    └── simple_fragment.glsl