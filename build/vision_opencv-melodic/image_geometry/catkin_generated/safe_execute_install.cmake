execute_process(COMMAND "/home/bal/catkin_ws/build/vision_opencv-melodic/image_geometry/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/bal/catkin_ws/build/vision_opencv-melodic/image_geometry/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
