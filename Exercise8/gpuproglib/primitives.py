import numpy as np


def create_plane():
    # Create the model
    rendVert = []
    rendFaces = []

    # Top Face
    # Vert1
    rendVert.append(-1.0)
    rendVert.append(0.0)
    rendVert.append(-1.0)
    rendVert.append(1.0)

    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(0.0)

    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(0.0)

    rendVert.append(0.0)
    rendVert.append(0.0)
    rendVert.append(1.0)

    rendVert.append(0.0)
    rendVert.append(0.0)

    # Vert2
    rendVert.append(-1.0)
    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(1.0)

    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(0.0)

    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(0.0)

    rendVert.append(0.0)
    rendVert.append(0.0)
    rendVert.append(1.0)

    rendVert.append(0.0)
    rendVert.append(1.0)

    # Vert3
    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(1.0)

    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(0.0)

    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(0.0)

    rendVert.append(0.0)
    rendVert.append(0.0)
    rendVert.append(1.0)

    rendVert.append(1.0)
    rendVert.append(1.0)

    # Vert4
    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(-1.0)
    rendVert.append(1.0)

    rendVert.append(0.0)
    rendVert.append(1.0)
    rendVert.append(0.0)

    rendVert.append(1.0)
    rendVert.append(0.0)
    rendVert.append(0.0)

    rendVert.append(0.0)
    rendVert.append(0.0)
    rendVert.append(1.0)

    rendVert.append(1.0)
    rendVert.append(0.0)

    # Face 1 indexs
    rendFaces.append(0)
    rendFaces.append(1)
    rendFaces.append(2)
    rendFaces.append(0)
    rendFaces.append(2)
    rendFaces.append(3)

    rendVert = np.array(rendVert)
    rendFaces = np.array(rendFaces)

    coordMin = np.array([-1.0, 0.0, -1.0])
    coordMax = np.array([1.0, 0.0, 1.0])

    return rendVert, rendFaces, coordMin, coordMax
