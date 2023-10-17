import sys
import os.path
import pyglet
import numpy as np
import OpenGL.GL.shaders
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as sh
import grafica.performance_monitor as pm
import grafica.lighting_shaders as ls

from grafica.gpu_shape import createGPUShape
from grafica.assets_path import getAssetPath

from OpenGL.GL import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Controller(pyglet.window.Window):

    def __init__(self, width, height, title="Tarea 2"):
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.fillPolygon = True
        #self.repeats = 0
        #coordenadas de cámara.
        self.showAxis = True
        self.viewPos = np.array([-10.0,10.0,10.0])
        self.at = np.array([0.0,0.0,0.0])
        self.camUp = np.array([0.0, 1.0, 0.0])
        #coordenadas update.
        self.rot = np.pi/100
        self.vel = 0.1
        self.anguloXZ = np.pi/2
        self.anguloY = 0
        #Se actualizan mediante los controles.
        self.mover = 0
        self.rotarXZ = 0
        self.rotarY = 0
        self.mouse_y = 0

    #recibe dos modelos, ya que naves y sombra se actualizan por separado.
    def update_escena(self,modelo1,modelo2):
        #Posiciones utilizadas para el mouse.
        if self.mouse_y > 1.5:
            self.rotarY = 1
        elif 1.3 > self.mouse_y > 0.7:
            self.rotarY = 0
        elif self.mouse_y < 0.5:
            self.rotarY = -1
        #Variables
        self.viewPos = np.array([-10.0,10.0,10.0])
        #Se da inicio al movimiento. 
        controller.anguloXZ += (self.rot * self.rotarXZ)
        controller.anguloY += (self.rot * self.rotarY)
        #transformaciones de la nave.
        modelo1.transform = tr.matmul([escuadron.transform,tr.rotationY(self.rot * self.rotarXZ)])
        modelo1.transform = tr.matmul([escuadron.transform,tr.rotationZ(self.rot * self.rotarY)])
        modelo1.transform = tr.matmul([escuadron.transform, tr.translate(self.mover/10,0,0)])
        #transformaciones de las sombras.
        modelo2.transform = tr.matmul([sombras.transform,tr.rotationY(self.rot * self.rotarXZ)])
        modelo2.transform = tr.matmul([sombras.transform, tr.translate(self.mover/10 * np.cos(self.anguloY),0.0,0.0)])
        
WIDTH, HEIGHT = 1000,1000
controller = Controller(width=WIDTH, height=HEIGHT)
#Color de fondo
glClearColor(0, 0, 0, 1.0)
glEnable(GL_DEPTH_TEST)
#Definimos los pipelines.
axisPipeline = sh.SimpleModelViewProjectionShaderProgram()
texPipeline = sh.SimpleTextureModelViewProjectionShaderProgram()
lightPipeline = ls.SimpleGouraudShaderProgram()

#Funciones de vista e iluminacion.
def setView(texPipeline, axisPipeline, lightPipeline):
    view = tr.lookAt(
            controller.viewPos,
            controller.at,
            controller.camUp,
        )

    glUseProgram(axisPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1], controller.viewPos[2])

def setPlot(texPipeline, axisPipeline, lightPipeline,posicionX,posicionZ):

    projection = tr.ortho(-8, 8, -8, 8, 0.1, 100) #camara ortografica
    #projection = tr.perspective(60, 1, 0.1, 100) #camara perspectiva

    glUseProgram(axisPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "lightPosition"), posicionX,20,posicionZ)
    
    glUniform1ui(glGetUniformLocation(lightPipeline.shaderProgram, "shininess"), 1000)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "constantAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "linearAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "quadraticAttenuation"), 0.001)

#Creacion del suelo texturado.
def createTexturedArc(d):
    vertices = [d, 0.0, 0.0, 0.0, 0.0,
                d+1.0, 0.0, 0.0, 1.0, 0.0]
    
    currentIndex1 = 0
    currentIndex2 = 1

    indices = []

    cont = 1
    cont2 = 1

    for angle in range(4, 185, 5):
        angle = np.radians(angle)
        rot = tr.rotationY(angle)
        p1 = rot.dot(np.array([[d],[0],[0],[1]]))
        p2 = rot.dot(np.array([[d+1],[0],[0],[1]]))

        p1 = np.squeeze(p1)
        p2 = np.squeeze(p2)
        
        vertices.extend([p2[0], p2[1], p2[2], 1.0, cont/4])
        vertices.extend([p1[0], p1[1], p1[2], 0.0, cont/4])
        
        indices.extend([currentIndex1, currentIndex2, currentIndex2+1])
        indices.extend([currentIndex2+1, currentIndex2+2, currentIndex1])

        if cont > 4:
            cont = 0


        vertices.extend([p1[0], p1[1], p1[2], 0.0, cont/4])
        vertices.extend([p2[0], p2[1], p2[2], 1.0, cont/4])

        currentIndex1 = currentIndex1 + 4
        currentIndex2 = currentIndex2 + 4
        cont2 = cont2 + 1
        cont = cont + 1

    return bs.Shape(vertices, indices)

def createTiledFloor(dim):
    vert = np.array([[-0.5,0.5,0.5,-0.5],[-0.5,-0.5,0.5,0.5],[0.0,0.0,0.0,0.0],[1.0,1.0,1.0,1.0]], np.float32)
    rot = tr.rotationX(-np.pi/2)
    vert = rot.dot(vert)

    indices = [
         0, 1, 2,
         2, 3, 0]

    vertFinal = []
    indexFinal = []
    cont = 0

    for i in range(-dim,dim,1):
        for j in range(-dim,dim,1):
            tra = tr.translate(i,0.0,j)
            newVert = tra.dot(vert)

            v = newVert[:,0][:-1]
            vertFinal.extend([v[0], v[1], v[2], 0, 1])
            v = newVert[:,1][:-1]
            vertFinal.extend([v[0], v[1], v[2], 1, 1])
            v = newVert[:,2][:-1]
            vertFinal.extend([v[0], v[1], v[2], 1, 0])
            v = newVert[:,3][:-1]
            vertFinal.extend([v[0], v[1], v[2], 0, 0])
            
            ind = [elem + cont for elem in indices]
            indexFinal.extend(ind)
            cont = cont + 4

    return bs.Shape(vertFinal, indexFinal)

def createStaticScene(pipeline):

    suelo = createGPUShape(pipeline, createTiledFloor(20))
    suelo.texture = sh.textureSimpleSetup(
        getAssetPath("textura2.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR_MIPMAP_NEAREST, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)
    
    sueloNode = sg.SceneGraphNode('suelo')
    sueloNode.transform = tr.scale(3,1,3)
    sueloNode.childs += [suelo]
    
    return sueloNode

#Funciones para leer el modelo 3D
def readFaceVertex(faceDescription):

    aux = faceDescription.split('/')

    assert len(aux[0]), "Vertex index has not been defined."

    faceVertex = [int(aux[0]), None, None]

    assert len(aux) == 3, "Only faces where its vertices require 3 indices are defined."

    if len(aux[1]) != 0:
        faceVertex[1] = int(aux[1])

    if len(aux[2]) != 0:
        faceVertex[2] = int(aux[2])

    return faceVertex

def readOBJ(filename, color):

    vertices = []
    normals = []
    textCoords= []
    faces = []

    with open(filename, 'r') as file:
        for line in file.readlines():
            aux = line.strip().split(' ')
            
            if aux[0] == 'v':
                vertices += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vn':
                normals += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'vt':
                assert len(aux[1:]) == 2, "Texture coordinates with different than 2 dimensions are not supported"
                textCoords += [[float(coord) for coord in aux[1:]]]

            elif aux[0] == 'f':
                N = len(aux)                
                faces += [[readFaceVertex(faceVertex) for faceVertex in aux[1:4]]]
                for i in range(3, N-1):
                    faces += [[readFaceVertex(faceVertex) for faceVertex in [aux[i], aux[i+1], aux[1]]]]

        vertexData = []
        indices = []
        index = 0

        # Per previous construction, each face is a triangle
        for face in faces:

            # Checking each of the triangle vertices
            for i in range(0,3):
                vertex = vertices[face[i][0]-1]
                normal = normals[face[i][2]-1]

                vertexData += [
                    vertex[0], vertex[1], vertex[2],
                    color[0], color[1], color[2],
                    normal[0], normal[1], normal[2]
                ]

            # Connecting the 3 vertices to create a triangle
            indices += [index, index + 1, index + 2]
            index += 3        

        return bs.Shape(vertexData, indices)

#Almacenamiento de los obj.
ASSETS = {
    "nave_nodriza": getAssetPath("nave_nodriza.obj"),
    "nave_hija": getAssetPath("nave_hija.obj"),
    "sombra": getAssetPath("sombra.obj"),
    "muros": getAssetPath("muros.obj"),
    "anillo": getAssetPath("anillos.obj"),
    "obstaculo": getAssetPath("obstaculos.obj"),
}
#creacion de la nave con grafo de escena.
def createScene(pipeline):

    # Creating shapes on GPU memory
    nave_principal = createGPUShape(pipeline, readOBJ(ASSETS["nave_nodriza"],(0.55,0.26,0.67)))
    nave_hija1 = createGPUShape(pipeline, readOBJ(ASSETS["nave_hija"],(0.18,0.52,0.75)))
    sombra = createGPUShape(pipeline, readOBJ(ASSETS["sombra"],(0,0,0)))
    muro = createGPUShape(pipeline, readOBJ(ASSETS["muros"],(0.15,0.7,0.38)))
    anillo = createGPUShape(pipeline, readOBJ(ASSETS["anillo"],(0.92,0.5,0.13)))
    obstaculo = createGPUShape(pipeline, readOBJ(ASSETS["obstaculo"],(0.92,0.3,0.23)))

    #Nave Nodriza
    nave1 = sg.SceneGraphNode("nave_nodriza")
    nave1.transform = tr.matmul([
                                tr.uniformScale(0.5),
                                tr.translate(0,3,0),
    
    ])
    nave1.childs += [nave_principal]

    #Nave izquierda
    hija1 = sg.SceneGraphNode("hija1")
    hija1.transform = tr.matmul([
                                tr.uniformScale(0.3),
                                tr.translate(-6,2,-7),
    
    ])
    hija1.childs += [nave_hija1]
    #Nave derecha
    hija2 = sg.SceneGraphNode("hija2")
    hija2.transform = tr.matmul([
                                tr.uniformScale(0.3),
                                tr.translate(-6,2,7),
    ])
    hija2.childs += [nave_hija1]
    #Sombras
    sombraNode = sg.SceneGraphNode("sombra")
    sombraNode.transform = tr.matmul([
                                tr.uniformScale(0.6),
                                tr.translate(-2.5,0.2,0)
    ])
    sombraNode.childs += [sombra]

    sombraNode2 = sg.SceneGraphNode("sombra2")
    sombraNode2.transform = tr.matmul([
                                tr.uniformScale(0.3),
                                tr.translate(-8,0.2,7)
    ])
    sombraNode2.childs += [sombra]

    sombraNode3 = sg.SceneGraphNode("sombra3")
    sombraNode3.transform = tr.matmul([
                                tr.uniformScale(0.3),
                                tr.translate(-8,0.2,-7)
                                
    ])
    sombraNode3.childs += [sombra]

    #Nodo naves
    naves = sg.SceneGraphNode("naves")
    naves.childs += [nave1]
    naves.childs += [hija1]
    naves.childs += [hija2]

    #Nodo sombras
    sombras = sg.SceneGraphNode("all_sombras")
    sombras.childs += [sombraNode]
    sombras.childs += [sombraNode2]
    sombras.childs += [sombraNode3]

    escuadron = sg.SceneGraphNode("escuadron")
    escuadron.childs += [naves]
    escuadron.childs += [sombras]

    #Muros
    muroNode = sg.SceneGraphNode("muro1")
    muroNode.transform = tr.matmul([
                                tr.translate(6,0,-12),
                                tr.uniformScale(0.6),
                                tr.rotationY(np.pi),
    ])
    muroNode.childs = [muro]

    muroNode2 = sg.SceneGraphNode("muro2")
    muroNode2.transform = tr.matmul([
                                tr.translate(6,0,6),
                                tr.uniformScale(0.6),
                                tr.rotationY(np.pi),
    ])
    muroNode2.childs = [muro]

    muroNode3 = sg.SceneGraphNode("muro3")
    muroNode3.transform = tr.matmul([
                                tr.translate(35,0,-12),
                                tr.uniformScale(0.6),
                                tr.rotationY(np.pi),
    ])
    muroNode3.childs = [muro]

    muroNode4 = sg.SceneGraphNode("muro4")
    muroNode4.transform = tr.matmul([
                                tr.translate(35,0,6),
                                tr.uniformScale(0.6),
                                tr.rotationY(np.pi),
    ])
    muroNode.childs = [muro]

    allmuros = sg.SceneGraphNode("all_muros")
    allmuros.childs += [muroNode]
    allmuros.childs += [muroNode2]
    allmuros.childs += [muroNode3]
    allmuros.childs += [muroNode4]

    #Anillo
    anilloNode = sg.SceneGraphNode("anillo")
    anilloNode.transform = tr.matmul([
                                tr.translate(10,-3,0),
                                tr.uniformScale(4),
                                tr.rotationY(np.pi/2),
    ])
    anilloNode.childs += [anillo]

    anilloNode2 = sg.SceneGraphNode("anillo")
    anilloNode2.transform = tr.matmul([
                                tr.translate(20,-3,0),
                                tr.uniformScale(4),
                                tr.rotationY(np.pi/2),
    ])
    anilloNode2.childs += [anillo]

    anillos = sg.SceneGraphNode("all_anillos")
    anillos.childs += [anilloNode]
    anillos.childs += [anilloNode2]

    obstaculoNode = sg.SceneGraphNode("obstaculo")
    obstaculoNode.transform = tr.matmul([
                                tr.translate(40,0,0.2),
                                tr.uniformScale(0.8),
                                tr.rotationY(np.pi/2),
    ])
    obstaculoNode.childs += [obstaculo]

    # All pieces together
    scene = sg.SceneGraphNode("escena")
    scene.childs += [escuadron]
    scene.childs += [allmuros]
    scene.childs += [anillos]
    scene.childs += [obstaculoNode]

    return scene

# Creating shapes on GPU memory
cpuAxis = bs.createAxis(7)
gpuAxis = sh.GPUShape().initBuffers()
axisPipeline.setupVAO(gpuAxis)
gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

#Creacion de la escena y suelo.
escena = createScene(lightPipeline) #escena completa
suelo = createStaticScene(texPipeline) #texturas del suelo

#Nodos a los que se le aplican transformaciones.
escuadron = sg.findNode(escena, "naves")
sombras = sg.findNode(escena, "all_sombras")

#Controles de la nave.
@controller.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.W:
        controller.mover += 1
    elif symbol == pyglet.window.key.S:
        controller.mover += -1
    elif symbol == pyglet.window.key.A:
        controller.rotarXZ += 1
    elif symbol == pyglet.window.key.D:
        controller.rotarXZ += -1
    elif symbol == pyglet.window.key.ESCAPE:
        controller.close()

@controller.event
def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.W:
        controller.mover += -1
    elif symbol == pyglet.window.key.S:
        controller.mover += 1
    elif symbol == pyglet.window.key.A:
        controller.rotarXZ += -1
    elif symbol == pyglet.window.key.D:
        controller.rotarXZ += 1
    elif symbol == pyglet.window.key.ESCAPE:
        controller.close()

#Controles del mouse.
@controller.event
def on_mouse_motion(x, y, dx, dy):
    controller.mouse_y = y/1000*2

def update(dt,controller):
    controller.total_time += dt

@controller.event
def on_draw():
    controller.clear()
    #esta linea se encarga de hacer las transformaciones.
    controller.update_escena(escuadron,sombras)
    #obtenemos la posicion de la nave y actualizamos la camara.
    posicion_nave = sg.findPosition(escena, "naves")
    controller.viewPos += np.array([posicion_nave[0][0],posicion_nave[1][0],posicion_nave[2][0]])
    controller.at = np.array([posicion_nave[0][0],posicion_nave[1][0],posicion_nave[2][0]])

    # Si el controller está en modo fillPolygon, dibuja polígonos. Si no, líneas.
    if (controller.fillPolygon):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    #llamamos a las funciones de vista e iluminación.
    setView(texPipeline, axisPipeline, lightPipeline)
    setPlot(texPipeline, axisPipeline, lightPipeline,posicion_nave[0][0],posicion_nave[2][0])
    
    if controller.showAxis:
            glUseProgram(axisPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            #axisPipeline.drawCall(gpuAxis, GL_LINES) # Dibuja los ejes

    # Dibujamos la escena
    glUseProgram(lightPipeline.shaderProgram)
    sg.drawSceneGraphNode(escena, lightPipeline, "model")
    # Dibujamos el suelo
    glUseProgram(texPipeline.shaderProgram)
    sg.drawSceneGraphNode(suelo, texPipeline, "model")
    
# Try to call this function 60 times per second
pyglet.clock.schedule(update, controller)
# Se ejecuta la aplicación
pyglet.app.run()