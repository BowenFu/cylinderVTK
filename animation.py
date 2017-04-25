from pyevtk.hl import gridToVTK, VtkGroup
import numpy
# Parameters
length = 20
diameter = 0.028
node_number = 81
start_time = 150.04
end_time = 159.96
time_step = .04
time_interval = 0.0004
skip_step = int(round(time_step / time_interval))

# Dimensions
radius_number, angle_number = 1, 90
radius_length, angle_length = diameter / 2, 360.0
radius_delta, angle_delta = (radius_length - 0.1 * diameter) / radius_number,\
    angle_length / angle_number

time, displacement_x, displacement_y = numpy.loadtxt('displacement.dat', unpack=True)
time.shape = -1, node_number
time = time[:,0]
time_select = (time >= start_time) & (time <= end_time)
time = time[time_select][::skip_step]
displacement_x.shape = -1, node_number
displacement_y.shape = -1, node_number
displacement_x = displacement_x[time_select][::skip_step]
displacement_y = displacement_y[time_select][::skip_step]
print(time.shape)

# Coordinates
radius_axis = numpy.arange(0, radius_length + 0.1 * radius_delta, radius_delta)
angle_axis = numpy.arange(0, angle_length + 0.1 * angle_delta, angle_delta)

x = numpy.zeros((radius_number + 1, angle_number + 1, node_number))
y = numpy.zeros((radius_number + 1, angle_number + 1, node_number))
z = numpy.zeros((radius_number + 1, angle_number + 1, node_number))

# Group
vtk_group = VtkGroup("riser/RiserGroup")
# cnt=0
for time_index in range(time.size):
    for k in range(node_number):
        # Nodal displacement
        x_deviation = displacement_x[time_index][k]
        y_deviation = displacement_y[time_index][k]
        z_deviation = k/float(node_number) * length
        #
        # Trans
        for j in range(angle_number + 1):
            for i in range(radius_number + 1):
                rad = numpy.radians(angle_axis[j])
                x[i, j, k] = radius_axis[i] * numpy.cos(rad) + x_deviation
                y[i, j, k] = radius_axis[i] * numpy.sin(rad) + y_deviation
                z[i, j, k] = z_deviation
    # Variables
    #
    # Output
    str1 = str(time_index)
    filename = 'riser/' + 'riser' + str1.zfill(4)
    filename_extension = filename + '.vts'
    gridToVTK(filename, x, y, z)

    vtk_group.addFile(filepath=filename_extension, sim_time=time[time_index])
vtk_group.save()
