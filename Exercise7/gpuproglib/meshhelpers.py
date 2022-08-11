import numpy as np

def read_model(myFile):
    vertexs = []
    normals = []
    faces = []
    currVertexs = []
    currNormals = []
    with open(myFile, 'r') as modelFile:        
        for line in modelFile:
            lineElements = line.split()
            if len(lineElements) > 0:
                if lineElements[0] == "v":
                    vertexs.append([float(lineElements[1]), float(lineElements[2]), float(lineElements[3])])
                elif lineElements[0] == "vn":
                    normals.append([float(lineElements[1]), float(lineElements[2]), float(lineElements[3])])
                elif lineElements[0] == "f":
                    vertex1 = lineElements[1].split('/')
                    vertex2 = lineElements[2].split('/')
                    vertex3 = lineElements[3].split('/')
                    faces.append([[int(vertex1[0])-1, int(vertex1[2])-1], [int(vertex2[0])-1, int(vertex2[2])-1], [int(vertex3[0])-1, int(vertex3[2])-1]])
    
    auxVertexs = np.array(vertexs)
    coordMax = np.amax(auxVertexs, axis=(0))
    coordMin = np.amin(auxVertexs, axis=(0))
    center = (coordMax + coordMin)*0.5
    auxVertexs = auxVertexs-center
    
    return auxVertexs.tolist(), normals, faces, coordMin, coordMax


def generate_rendering_buffers(vertexs, normals, faces):
    rendVerts = []
    renderIndexs = []
    indexDict = {}
    for face in faces:
        vert1 = face[0]
        indexVert1 = len(rendVerts)//7
        if str(vert1) in indexDict:
            indexVert1 = indexDict[str(vert1)]
        else:
            indexDict[str(vert1)] = indexVert1
            rendVerts.append(vertexs[vert1[0]][0])
            rendVerts.append(vertexs[vert1[0]][1])
            rendVerts.append(vertexs[vert1[0]][2])
            rendVerts.append(1.0)
            rendVerts.append(normals[vert1[1]][0])
            rendVerts.append(normals[vert1[1]][1])
            rendVerts.append(normals[vert1[1]][2])

        vert2 = face[1]
        indexVert2 = len(rendVerts)//7
        if str(vert2) in indexDict:
            indexVert2 = indexDict[str(vert2)]
        else:
            indexDict[str(vert2)] = indexVert2
            rendVerts.append(vertexs[vert2[0]][0])
            rendVerts.append(vertexs[vert2[0]][1])
            rendVerts.append(vertexs[vert2[0]][2])
            rendVerts.append(1.0)
            rendVerts.append(normals[vert2[1]][0])
            rendVerts.append(normals[vert2[1]][1])
            rendVerts.append(normals[vert2[1]][2])

        vert3 = face[2]
        indexVert3 = len(rendVerts)//7
        if str(vert3) in indexDict:
            indexVert3 = indexDict[str(vert3)]
        else:
            indexDict[str(vert3)] = indexVert3
            rendVerts.append(vertexs[vert3[0]][0])
            rendVerts.append(vertexs[vert3[0]][1])
            rendVerts.append(vertexs[vert3[0]][2])
            rendVerts.append(1.0)
            rendVerts.append(normals[vert3[1]][0])
            rendVerts.append(normals[vert3[1]][1])
            rendVerts.append(normals[vert3[1]][2])

        renderIndexs.append(indexVert1)
        renderIndexs.append(indexVert2)
        renderIndexs.append(indexVert3)
    return np.array(rendVerts), np.array(renderIndexs)