import numpy as np
import cv2 as cv
import scipy.spatial as spatial
import scipy.cluster as cluster
from collections import defaultdict
import pieceClassification

def write_crop_images(resized, points):
    points_np= np.array(points, dtype=int)
    #Creo una matrice dei punti
    points_np= np.reshape(points_np,(9,9,2))
    image_list=[]
    point_d = points_np[0][1][0] - points_np[0][0][0]
    for i in range(8):
        for j in range(8):
            sq=resized[points_np[i][j][1]:points_np[i][j][1]+point_d,points_np[i][j][0]:points_np[i][j][0]+point_d]
            image_list.append(sq)

    return image_list



# Find the intersections of the lines
def line_intersections(h_lines, v_lines):
    points = []
    for r_h, t_h in h_lines:
        for r_v, t_v in v_lines:
            a = np.array([[np.cos(t_h), np.sin(t_h)], [np.cos(t_v), np.sin(t_v)]])
            b = np.array([r_h, r_v])
            inter_point = np.linalg.solve(a, b)
            points.append(inter_point)
    return np.array(points)


# Separate line into horizontal and vertical
def h_v_lines(lines):
    h_lines, v_lines = [], []
    for rho, theta in lines:
        if theta < np.pi / 4 or theta > np.pi - np.pi / 4:
            v_lines.append([rho, theta])
        else:
            h_lines.append([rho, theta])
    return h_lines, v_lines

# Hierarchical cluster (by euclidean distance) intersection points
#Non mi è ben chiaro cosa faccia, penso raggruppi le celle ma vabbè vedremo
def cluster_points(points):
    dists = spatial.distance.pdist(points)
    single_linkage = cluster.hierarchy.single(dists)
    flat_clusters = cluster.hierarchy.fcluster(single_linkage, 15, 'distance')
    cluster_dict = defaultdict(list)
    for i in range(len(flat_clusters)):
        cluster_dict[flat_clusters[i]].append(points[i])
    cluster_values = cluster_dict.values()
    clusters = map(lambda arr: (np.mean(np.array(arr)[:, 0]), np.mean(np.array(arr)[:, 1])), cluster_values)
    return sorted(list(clusters), key=lambda k: [k[1], k[0]])




def points_original_image(points):
    points_np= np.array(points, dtype=float)
    for point in  points_np:
        point[0]=point[0]/0.3
        point[1]=point[1]/0.3
    return points_np

########################################################################################################################

########################################################################################################################


#da qua inizia il codice dello scrypt
#ritorna la lista delle immagini separeate

def board_detect(path):
    img = cv.imread(path,cv.IMREAD_UNCHANGED)
    start_height = img.shape[0] / 4
    finish_height = start_height + img.shape[0] / 2 + img.shape[0] / 8
    img = img[int(start_height):int(finish_height), :]  # magari farlo in proporzione

    scale_percent = 30 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    resized= cv.blur(resized,(2,3))
    gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray,50,150,apertureSize = 3)
    lines = cv.HoughLines(edges,0.2,np.pi/180,180)

    lines = np.reshape(lines, (-1, 2))
    h_lines, v_lines = h_v_lines(lines)
    intersection_points=line_intersections(h_lines,v_lines)
    points=cluster_points(intersection_points)

    points=points_original_image(points)
    img_list=write_crop_images(img, points)

    img_list_np = np.asarray(img_list)
    img_list_np = np.reshape(img_list_np, (8, 8, 127, 127, 3))
    return img_list_np



