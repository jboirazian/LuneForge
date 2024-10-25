# LuneForge
[![Featured on Hacker News](https://hackerbadge.now.sh/api?id=41425675)](https://news.ycombinator.com/item?id=41425675)
<p align="center">
  <img src="https://github.com/jboirazian/LuneForge/assets/21143405/c74157f0-7896-45e1-a5f4-219d3b1a810d" alt="LuneForge" width="500"/>
</p>



## What is LuneForge?

**TLDR**: an Open-Source Software for Designing 3D-Printable Luneburg Lenses for RF Applications

LuneForge is a cutting-edge **work in progress** open-source tool designed for creating precise Luneburg lens models tailored for radio frequency (RF) applications, optimized for SLA 3D printing. Ideal for RF engineers, hobbyists, and researchers, LuneForge simplifies the design process with user-friendly features and customizable parameters. Enhance your RF projects with advanced lens designs, improve signal focusing and directionality, and join a community of innovators in the field of radio frequency technology.

## Screenshots

![image](https://github.com/user-attachments/assets/4bcfc710-36c8-4828-9a6e-e17417089945)




https://github.com/user-attachments/assets/7037960c-ab61-4e32-aaee-4b98a8713ff3





## Features + Roadmap

- [x] Lightweight and fast generation of Luneburg lenses
- [x] Elegant Web base UI
- [x] Export generated image to .stl file for 3D printing
- [x] Export generated image to .obj file for CST studio
- [ ] Release online demo 
- [ ] Material DRC Check  
- [ ] Ability to introduce multiple lattice unti cells for the lens generation
- [x] DockerHub image for fast instalation
- [ ] Multi Lens generation
- [ ] Integration with CST Studio
- [ ] And many more !


## Get started:

For the following , it is required to have [Docker](https://www.docker.com/) installed 

Install from Dockerhub (recommended):

```bash
docker run --name luneforge -v $(pwd)/models:/app/static/models juanboirazian/luneforge

```

Install from source:

```bash
git clone https://github.com/jboirazian/LuneForge
```

```bash
cd LuneForge
```

```bash
docker compose up --build
```


## Tech Stack

**Client:** HTMX, DaisyUI

**Server:** Flask , Pymesh

## Contact information:

- Email: jboirazian@frba.utn.edu.ar
- Linkdin : https://www.linkedin.com/in/juan-boirazian/ 
