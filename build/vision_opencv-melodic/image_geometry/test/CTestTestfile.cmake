# CMake generated Testfile for 
# Source directory: /home/bal/catkin_ws/src/vision_opencv-melodic/image_geometry/test
# Build directory: /home/bal/catkin_ws/build/vision_opencv-melodic/image_geometry/test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_image_geometry_nosetests_directed.py "/home/bal/catkin_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/bal/catkin_ws/build/test_results/image_geometry/nosetests-directed.py.xml" "--return-code" "\"/usr/bin/cmake\" -E make_directory /home/bal/catkin_ws/build/test_results/image_geometry" "/usr/bin/nosetests-2.7 -P --process-timeout=60 /home/bal/catkin_ws/src/vision_opencv-melodic/image_geometry/test/directed.py --with-xunit --xunit-file=/home/bal/catkin_ws/build/test_results/image_geometry/nosetests-directed.py.xml")
add_test(_ctest_image_geometry_gtest_image_geometry-utest "/home/bal/catkin_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/bal/catkin_ws/build/test_results/image_geometry/gtest-image_geometry-utest.xml" "--return-code" "/home/bal/catkin_ws/devel/lib/image_geometry/image_geometry-utest --gtest_output=xml:/home/bal/catkin_ws/build/test_results/image_geometry/gtest-image_geometry-utest.xml")
