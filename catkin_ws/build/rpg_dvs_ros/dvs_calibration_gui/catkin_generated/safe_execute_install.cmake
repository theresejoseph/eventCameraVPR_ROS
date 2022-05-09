execute_process(COMMAND "/home/tresjsph/catkin_ws/build/rpg_dvs_ros/dvs_calibration_gui/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/tresjsph/catkin_ws/build/rpg_dvs_ros/dvs_calibration_gui/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
