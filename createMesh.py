#with poroelastic
cubit.cmd('reset')
import sys
import os
sys.path.append("D:\\SEMFAULTS\\Cubits\\CUBIT_GEOCUBIT\\geocubitlib")
import absorbing_boundary
import save_fault_nodes_elements
import cubit2specfem3d
#import boundary_definition

km = 10
z_surf = 0*km

####  initializing coordinates x,y,z
x = []     # fault
y = []
z = []

xbulk = [] # bulk
ybulk = []
zbulk = []

xbulk.append(-75*km)   #x1
xbulk.append(75*km)    #x2
xbulk.append(75*km)    #x3
xbulk.append(-75*km)   #x4

ybulk.append(-75*km)  #y1
ybulk.append(-75*km)  #y2
ybulk.append(75*km)   #y3
ybulk.append(75*km)   #y4

zbulk = [z_surf]*4

x.append(-30*km) #x5
x.append(0*km)   #x6
x.append(30*km)  #x7
x.append(0*km)   #x8

y.append(0.0)       #y5
y.append(0.1)    #y6
y.append(0.0)       #y7
y.append(-0.1)   #y8

z = [z_surf]*4

# current work directory
cubit.cmd('pwd')

# Creating the volumes
cubit.cmd('reset')

####################  bulk ###########################################
for i in range(len(xbulk)):
   vert="create vertex x "+str(xbulk[i])+" y "+str(ybulk[i])+" z "+str(zbulk[i])
   cubit.cmd(vert)

################  Loading fault points profile#############################
for i in range(len(x)):
  vert="create vertex x "+str(x[i])+" y "+str(y[i])+" z "+str(z[i])
  cubit.cmd(vert)

################ creating fault domains #################################
bulk1="create curve vertex 1 2"
bulk2="create curve vertex 2 3"
bulk3="create curve vertex 3 4"
bulk4="create curve vertex 4 1"

fault_up="create curve spline vertex 5 6 7"
fault_down="create curve spline vertex 5 8 7"

cubit.cmd(bulk1)
cubit.cmd(bulk2)
cubit.cmd(bulk3)
cubit.cmd(bulk4)

cubit.cmd(fault_up)
cubit.cmd(fault_down)

surface="create surface curve 1 2 3 4 5 6"
cubit.cmd(surface)

cubit.cmd("sweep surface 1  vector 0  0 1 distance "+str(140*km))
cubit.cmd("sweep curve 5 vector 0 0 1 distance "+str(30*km))
cubit.cmd("sweep curve 6 vector 0 0 1 distance "+str(30*km))


#############################################


cubit.cmd('#create stope')
cubit.cmd('brick x 400 y 100 z 100')
cubit.cmd('move Volume 4 x -150 y -300 z 850 include_merged ')
cubit.cmd('subtract body 4 from body 1  keep')
cubit.cmd('del old orebody again')
cubit.cmd('del vol 1')

cubit.cmd('webcut volume 5 4 with general plane xy offset 850  ')
cubit.cmd('webcut body 6  with general plane xy offset 400  ')
cubit.cmd('webcut body 5  with general plane xy offset 1100  ')

cubit.cmd('merge tolerance 1e-3')
cubit.cmd('imprint all')
cubit.cmd('merge all')

cubit.cmd('#del fault auxi')
cubit.cmd('delete body 2 3')

cubit.cmd('vol 4 size 25 ')
cubit.cmd('#vol 4 scheme map')
cubit.cmd('mesh vol 4')

cubit.cmd('vol 9 size 50 ')
cubit.cmd('mesh vol 9')

cubit.cmd('#draw volume 5')
cubit.cmd('vol 5 size 50')
cubit.cmd('mesh volume 5')

cubit.cmd('vol 7 size 25')
cubit.cmd('mesh volume 7')

cubit.cmd('draw vol 6')
cubit.cmd('vol 6 size 50')
cubit.cmd('mesh volume 6')

cubit.cmd('vol 8 size 50')
cubit.cmd('mesh volume 8')

cubit.cmd('#unite stope')
cubit.cmd('unite volume 4 7 include_mesh ')
cubit.cmd('#unite orebody profile')
cubit.cmd('unite volume 6 9 include_mesh ')

#############################change interface to python#############
os.system('mkdir -p MESH')

########### Fault elements and nodes ###############
# fault surfaces (up/down)
Au = [9]
Ad = [10]

faultA = save_fault_nodes_elements.fault_input(1,Au,Ad)


entities=['face']
absorbing_boundary.define_parallel_bc(entities) # in absorbing_boundary.py

#################Define material properties for the 4 volumes##################
cubit.cmd('#### DEFINE MATERIAL PROPERTIES #######################')


#assign materials properties
cubit.cmd('#### DEFINE MATERIAL PROPERTIES #######################')

cubit.cmd('block 1 name "acoustic 1" ')       # Stope acoustic material region
cubit.cmd('block 1 attribute count 4')
cubit.cmd('block 1 attribute index 1 1  ')     # material 1
cubit.cmd('block 1 attribute index 2 343 ')  # vp
cubit.cmd('block 1 attribute index 3 0 ')      # vs
cubit.cmd('block 1 attribute index 4 1.225 ')  # rho

cubit.cmd('block 2 name "elastic 1" ')         # Sandstone elastic material 
cubit.cmd('block 2 attribute count 6')
cubit.cmd('block 2 attribute index 2 1')       # material 2
cubit.cmd('block 2 attribute index 2 1127')    # vp
cubit.cmd('block 2 attribute index 3 500')    # vs
cubit.cmd('block 2 attribute index 4 2350')    # rho
cubit.cmd('block 2 attribute index 5 50')      # Qmu
cubit.cmd('block 2 attribute index 6 0')        # anisotropy_flag

cubit.cmd('block 3 name "elastic 2" ')       # bedrock elastic material region
cubit.cmd('block 3 attribute count 6')
cubit.cmd('block 3 attribute index 1 3  ')       # material 3
cubit.cmd('block 3 attribute index 2 1481 ')     # vp
cubit.cmd('block 3 attribute index 3 912 ')     # vs
cubit.cmd('block 3 attribute index 4 2800 ')     # rho
cubit.cmd('block 3 attribute index 5 91')         # Q_mu
cubit.cmd('block 3 attribute index 6 0 ')        # anisotropy_flag

cubit.cmd('block 4 name "poroelastic 1" ')       # Orebody poroelastic material region (will be fully defined in nummaterial_poroelastic_file)
cubit.cmd('block 4 attribute count 7')
cubit.cmd('block 4 attribute index 1 4  ')       # material 4
cubit.cmd('block 4 attribute index 2 1322 ')     # vp
cubit.cmd('block 4 attribute index 3 710 ')     # vs
cubit.cmd('block 4 attribute index 4 2670 ')     # rho
cubit.cmd('block 4 attribute index 5 142')    # Q_kappa
cubit.cmd('block 4 attribute index 6 71')       # Q_mu
cubit.cmd('block 4 attribute index 7 0 ')        # anisotropy_flag

#cubit.cmd('block 4 name "elastic 4" ')       # Orebody elastic material region
#cubit.cmd('block 4 attribute count 6')
#cubit.cmd('block 4 attribute index 1 4  ')       # material 4
#cubit.cmd('block 4 attribute index 2 1127 ')     # vp
#cubit.cmd('block 4 attribute index 3 500 ')     # vs
#cubit.cmd('block 4 attribute index 4 2350 ')     # rho
#cubit.cmd('block 4 attribute index 5 50')       # Q_mu
#cubit.cmd('block 4 attribute index 6 0 ')        # anisotropy_flag

##########Export to SPECFEM3D format using cubit2specfem3d.py of GEOCUBIT#########

cubit2specfem3d.export2SPECFEM3D('MESH')

cubit.cmd('#fault nodes')
cubit.cmd('#Node 25814 25816 25818 25824 25826 25828 25834 25836 25838 25849 25851 25853')
cubit.cmd('group "faultStations" add node 25814 25816 25818 25824 25826 25828 25834 25836 25838 25849 25851 25853')

cubit.cmd('#bedrock nodes')
cubit.cmd('#Node 25179 25253 25491 25652 25719 25728')
cubit.cmd('group "BedrockStations" add node 25179 25253 25491 25652 25719 25728')

cubit.cmd('#stope nodes')
cubit.cmd('#Node 108 114 162 164 180 182 198 204 14755 14761 14840 14846')
cubit.cmd('group "StopeStations" add node 108 114 162 164 180 182 198 204 14755 14761 14840 14846')

cubit.cmd('#sandstone nodes')
cubit.cmd('#Node 13849 13902 13949 14076 14563 14585')
cubit.cmd('group "SandstoneStations" add node 13849 13902 13949 14076 14563 14585')

cubit.cmd('#nucleation nodes - along strike x')
cubit.cmd('group "NucleationNodes" add node 25769 25787 25793 25794 25795 25796 25797 25798 25799 25800 25801 25802 25803')

cubit.cmd('disp all')

#######To create a different mesh. Follow the analogy herein. Using the webcut tool in Coreform Cubit generates a locked fault-plane (December, 2024).