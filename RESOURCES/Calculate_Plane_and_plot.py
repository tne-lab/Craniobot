
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

##################################################
# CALCULATE PLANE FROM 3 or more points
##################################################


def best_plane_from_points(xs,ys,zs):# xs, ys, zs are series of points

        # do fit
        tmp_A = []
        tmp_b = []
        for i in range(len(xs)):
            tmp_A.append([xs[i], ys[i], 1])
            tmp_b.append(zs[i])
        b = np.matrix(tmp_b).T
        A = np.matrix(tmp_A)
        # The following finds the best fit of a plane to the given points.
        fit_plane = (A.T * A).I * A.T * b
        errors = b - A * fit_plane
        residual = np.linalg.norm(errors)
        return fit_plane, errors, residual


def draw_circle(ctrx,ctry,ctrz, r,plane,num_points=16):
     ptx = []
     pty = []
     ptz = []
     points = []

     deg_per_point = 360.0/num_points
     for a in np.arange(0,361,.5):
         x = ctrx + r * np.cos(a*np.pi/180.0)
         y = ctry + r * np.sin(a*np.pi/180.0)
         if plane is not None:
             zmtx = plane[0][0]*x + plane[1][0]* y + plane[2][0]
             z = float("%f" % zmtx) # Romoves brackets from z, "[[z]]"
         else:
             z = ctrz      
         if a%22.5 == 0.0:# 16 point circle = 360/22.5
                 ptx.append(x)
                 pty.append(y)
                 ptz.append(z)
                 points.append((x,y,z))
                 print ("num points: ",len(points))        
     return ptx,pty,ptz,points
        
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
      
##############################################################################
#   CALCULATE BEST FIT PLANE, PROJECTED CIRCLE
##############################################################################
def best_fit_plot(xs,ys,zs,radius,Bregma,x_offset,y_offset):

        if len(xs) >3:
                fit_plane, errors, residual = best_plane_from_points(xs,ys,zs)
                print("plane :",fit_plane)

                # plot raw data
                plt.figure()
                ax = plt.subplot(111, projection='3d')
                ax.scatter(xs, ys, zs, color='b')
                print ("solution:")
                print ("%f x + %f y + %f = z" % (fit_plane[0], fit_plane[1], fit_plane[2]))
                print ("errors:")
                print (errors)
                print ("residual:")
                print (residual)

                # plot plane
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                X,Y = np.meshgrid(np.arange(xlim[0], xlim[1]),
                                  np.arange(ylim[0], ylim[1]))
                Z = np.zeros(X.shape)
                for r in range(X.shape[0]):
                    for c in range(X.shape[1]):
                        Z[r,c] = fit_plane[0] * X[r,c] + fit_plane[1] * Y[r,c] + fit_plane[2]

                # DRAW CIRCLE
                ptx,pty,ptz, points = draw_circle(Bregma[0]+x_offset, Bregma[1]-y_offset,Bregma[2],radius,fit_plane)
                #ax.scatter(ptx, pty, 0, color='b')

                #Project Circle onto best-fit plane
                ax.scatter(ptx, pty, ptz, color='r')

                # Draw Graph
                ax.plot_wireframe(X,Y,Z, color='k')
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('z')
                plt.show()
        else: # Assume rat skull is parallel to horizontal plane
                ptx,pty,ptz, points = draw_circle(Bregma[0]+x_offset, Bregma[1]-y_offset,Bregma[2],radius,None)
                

        return points


