#-- my_code_hw01.py
#-- hw01 GEO1015.2020
#-- Pratyush Kumar
#-- 5359252
#-- Simon Pena Pereira
#-- 5391210


#-- import outside the standard Python library are not allowed, just those:
#%%
import math
import numpy as np
import scipy.spatial
import startin 
#-----

#%%
def raster_frame_creator(np_list ,cellsize):
    """returns raster as a 1d array (list of all coordinates of pixels referring to lower left)
    the no of cells as a tuple and the bounding box         

    Args:
        np_list ([numpy array]): [numpy array of list of lists sent to function]
        cellsize ([float]): [cellsize as processed and passed on to main function]
    """
    #compute bbox 
    x_list = np_list[:,0].copy()
    y_list = np_list[:,1].copy()
    z_list = np_list[:,2].copy()
    
    xmin, xmax, ymin, ymax = x_list.min(), x_list.max(), y_list.min(), y_list.max()

    #determine no of cells and create bbox
    no_x, no_y = 0, 0

    if (xmax-xmin)%cellsize == 0:
        no_x = int((xmax-xmin)//cellsize)
    else:
        no_x = int((xmax-xmin)//cellsize) +1

    if (ymax-ymin)%cellsize == 0:
        no_y = int((ymax-ymin)//cellsize)
    else:
        no_y = int((ymax-ymin)//cellsize) +1
    
    bbox = ((xmin,ymin) , (xmin + no_x*cellsize , ymin + no_y*cellsize))

    #raster creation
    rast_x = np.arange(bbox[0][0],bbox[1][0], cellsize)
    rast_y = np.arange(bbox[0][1],bbox[1][1], cellsize)
    rast_x = np.flip(rast_x)

    rast_coord = np.array([[i,j] for i in rast_x for j in rast_y])

    return(rast_coord , z_list , (no_x, no_y) , bbox)

# def raster_writer(rast_nm):

#%%
def nn_interpolation(list_pts_3d, j_nn):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with nearest neighbour interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_nn:        the parameters of the input for "nn"
    Output:
        returns the value of the area
 
    """  
    print("cellsize:", j_nn['cellsize'])
    cellsize =  float(j_nn['cellsize'])
    #compute bbox     #convert list3d to numpy array find min and max coordinates
    np_list = np.array(list_pts_3d)
    #make raster frame as 1d
    rast_coord , z_list,(no_x,no_y) ,bbox= raster_frame_creator(np_list , cellsize)
    xmin , ymin = bbox[0]

    list_pts = np_list[:,[0,1]]
    kd = scipy.spatial.KDTree(list_pts)
    
    rast_z = []
    
    for coord in rast_coord:
        _ , indx = kd.query(coord, k=1)
        rast_z.append(z_list[indx])
    
    #to put in the interpolation for z values
    rast_z=np.array(rast_z)
    rast_z=rast_z.reshape(int(no_x), int(no_y))

    #convex hull set anything outside it as     
    #create convex hull
    hull = scipy.spatial.ConvexHull(list_pts)

    ##writing asc file
    fh = open(j_nn['output-file'], "w")
    fh.write(f"NCOLS {no_y}\nNROWS {no_x}\nXLLCORNER {xmin}\nYLLCORNER {ymin}\nCELLSIZE {cellsize}\nNODATA_VALUE{-9999}\n") 
    for i in rast_z:
        fh.write(" ".join([str(_) for _ in i]) + '\n')
    fh.close()
    print("File written to", j_nn['output-file'])


#%%
def idw_interpolation(list_pts_3d, j_idw):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with IDW
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_idw:       the parameters of the input for "idw"
    Output:
        returns the value of the area
 
    """  
    # print("cellsize:", j_idw['cellsize'])
    # print("radius:", j_idw['radius'])

    #-- to speed up the nearest neighbour us a kd-tree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html#scipy.spatial.KDTree
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query
    # kd = scipy.spatial.KDTree(list_pts)
    # i = kd.query_ball_point(p, radius)
    
    print("File written to", j_idw['output-file'])

#%%
def tin_interpolation(list_pts_3d, j_tin):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with linear in TIN interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_tin:       the parameters of the input for "tin"
    Output:
        returns the value of the area
 
    """  
    #take params and create a raster outline as in nn
    cellsize =  float(j_tin['cellsize'])
    np_list = np.array(list_pts_3d)
    
    rast_coord , z_list,(no_x,no_y) ,bbox= raster_frame_creator(np_list , cellsize)
    xmin , ymin = bbox[0]


    #-- example to construct the DT with scipy
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html#scipy.spatial.Delaunay
    dt = scipy.spatial.Delaunay(np_list[:,[0,1]])

    #-- example to construct the DT with startin
    # minimal docs: https://github.com/hugoledoux/startin_python/blob/master/docs/doc.md
    # how to use it: https://github.com/hugoledoux/startin_python#a-full-simple-example
    # you are *not* allowed to use the function for the tin linear interpolation that I wrote for startin
    # you need to write your own code for this step
    # but you can of course read the code [dt.interpolate_tin_linear(x, y)]
    
    print("File written to", j_tin['output-file'])

#%%
def kriging_interpolation(list_pts_3d, j_kriging):
    """
    !!! TO BE COMPLETED !!!
     
    Function that writes the output raster with ordinary kriging interpolation
     
    Input:
        list_pts_3d: the list of the input points (in 3D)
        j_kriging:       the parameters of the input for "kriging"
    Output:
        returns the value of the area
 
    """  
    
    
    print("File written to", j_kriging['output-file'])
