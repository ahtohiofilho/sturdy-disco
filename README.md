# sturdy-disco

# Sphere-Based Civilization Game

> A prototype civilization simulation game rendered on a spherical world, built with modern OpenGL using Python.

This project aims to create a 3D spherical world for strategy and civilization gameplay, using **OpenGL** for rendering and **GLFW** for window and input management. The current implementation provides the foundation for rendering a **polyhedral sphere** (Goldberg G(n,0)) composed of **hexagons and pentagons**, with biome-based coloring and orbit camera controls.

---

## 🌍 Current State

### ✅ Core Features Implemented:
- **Window Management**:  
  - Fullscreen OpenGL context setup using GLFW  
  - Modular class-based structure (`Window` class)  
  - Graceful shutdown via ESC key  

- **Shader System**:  
  - Class-based shader manager (`Shader`)  
  - Support for dynamic uniform updates (projection/view matrices)  
  - Ready for lighting or texturing extensions  

- **3D Spherical World Rendering**:  
  - Generation of a Goldberg polyhedron (G(2,0)) with 12 pentagons and multiple hexagons  
  - Each polygon is colored according to its biome type (e.g., prairie, ocean, desert)  
  - Rendered using `GL_TRIANGLE_FAN` per face for accurate topology  

- **Camera System**:  
  - Orbit-style camera with yaw/pitch control via keyboard  
  - Dynamic view matrix generation using `pyglm`  

- **Geographic Data Engine**:  
  - Biome classification based on altitude, moisture, and solar incidence  
  - Movement cost and agricultural productivity assigned per biome  
  - Graph-based representation of regions and connections  

- **Modular Architecture**:  
  - Clean separation of concerns across modules:  
    - `contexto.py`: global state and integration point  
    - `renderer.py`: rendering pipeline  
    - `geografia.py`: geography engine  
    - `poligonos.py`: polyhedron geometry generator  

---

## 🎯 Future Goals

- [ ] Add interactive UI for selecting provinces  
- [ ] Implement resource management and civilization mechanics  
- [ ] Enable smooth zoom and continuous rotation
- [ ] Export map as JSON or SVG  

---

## 🧰 Dependencies

Install required packages using pip:

```bash
pip install glfw PyOpenGL networkx numpy pyglm

## 📁 Project Structure

sturdy-disco/
├── main.py # Entry point: creates Window instance and runs the app
├── contexto.py # Central Context object that holds geografia, camera, and renderer
├── window.py # Manages GLFW lifecycle and input callbacks
├── rendering/
│ ├── shader.py # Shader compilation and usage logic
│ ├── renderer.py # Renderer class with VAO/VBO and draw loop
│ └── buffers.py # Buffer preparation for OpenGL
├── utils/
│ ├── polygons.py # Generates 3D coordinates for polyhedron faces
│ └── geography.py # Biome assignment, graph definition, and node metadata
└── shaders/
├── render_vs.glsl # Vertex shader with projection/view uniforms
├── render_fs.glsl # Fragment shader with flat color output
├── picking_vs.glsl # Vertex shader for polygon selection (unique color pass)
└── picking_fs.glsl # Fragment shader that assigns unique RGB color per polygon