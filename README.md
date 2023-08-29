# Kanzi-Arrow-Warp - Graphic Warping Algorithm using GLSL & C++

A warping algorithm for sending a single point from a projection arrow to its warped location, simulated in Kanzi engine and run on GPU, for individual points in parallel.

I wrote a graphic warping algorithm using GLSL and C++ within the Kanzi Studio environment. The program warps and projects a navigation arrow onto road imagery, resulting in a visually dynamic navigation aid. The program is to be applied onto AR-HUD products. Incorporated bezier curves and certain vector calculus principles to enhance the accuracy and realism of the warping effect.

## Key Features

- Accurate graphic warping and projection of navigation arrow onto road imagery.
- Bezier curve integration to enhance warping precision and realism.
- Used C++ to generate coordinates, stored in a "log" file, that represents generated and "warped" coordinates, while using GLSL to implement the actual program in Kanzi.

### Prerequisites

- Kanzi Studio environment
- C++ compiler
- OpenGL support

## Demonstration

- Asked GPT for a python script to plot my C++ simulation results. Sample: ![demonstration](/Plotting/plots/start_plot.png "demonstration") ![demonstration](/Plotting/plots/fix2_plot.png "demonstration")
- Visual results for the GLSL implementation in the Demo directory.
![demonstration](/Demo/demo_arrow1.png "demonstration")
![demonstration](/Demo/demo_arrow2.png "demonstration")
![demonstration](/Demo/demo_code.png "demonstration")
![demonstration](/Demo/demo_control_points.png "demonstration")
