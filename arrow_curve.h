/*

This file stores the necessary functions to create a curve with given points.

*/


#include "point.h"


using namespace std;


constexpr double DIV_PARAMETER = 10; // Optimally 10.
constexpr double SCALE = 0.5; // Optimally 0.5.
constexpr double HALF_WIDTH = 0.3; // Optimally 0.3.


// The function b(t, b0, b1, b2) that produces v_t, the Bezier curve's position vector at time t.
point<double> bezier(double t, point<double> b0, point<double> b1, point<double> b2) {
	point<double> v_t = b0*(1-t)*(1-t) + b1*(2*t)*(1-t) + b2*t*t;
	return v_t;
}


// Adding middle points to every interval to aid the curve production.
vector<point<double>> transform_raw_points(const vector<point<double>>& raw_points) {
	vector<point<double>> trans; trans.push_back(raw_points[0]);

	unsigned int i = 1;
	for (; i < raw_points.size()-2; ++i) {
		point<double> v1 = raw_points[i]; point<double> v2 = raw_points[i + 1];
		point<double> v_mid = v1*SCALE + v2*(1-SCALE);
		trans.push_back(v1); trans.push_back(v_mid);
	}

	trans.push_back(raw_points[i]); trans.push_back(raw_points[i + 1]);

	return trans;
}


// Inputs: an array of points, transformed state.
// Output: the more detailed, Bezier curve version. A vector of points.
vector<point<double>> produce_curve(const vector<point<double>>& trans) {
	
	vector<point<double>> curve;

	// Iterate through, 3 points at a time.
	for (unsigned int i = 0; i < trans.size()-2; i += 2) { // Jumps 2 to make the Bezier curve.
		point<double> b0 = trans[i], b1 = trans[i + 1], b2 = trans[i + 2];

		// Now build points through Bezier.
		for (double t = 0; t < 1 - (1 / DIV_PARAMETER); t += 1 / DIV_PARAMETER) {
			curve.push_back(bezier(t, b0, b1, b2));
		}
	}

	return curve;
}


// Takes a vector of points, our central curve, and creates the left part.
vector<point<double>> produce_left(const vector<point<double>>& curve) {
	vector<point<double>> curve_left;

	// Initialize & add the first one.
	point<double> start = curve[0]; start.x -= HALF_WIDTH;
	curve_left.push_back(start);
	
	// Iterate through.
	point<double> u;
	for (int i=1; i<curve.size(); ++i) {
		// These are slightly harder to understand. Explanation in PDF.
		point<double> p = curve[i];
		point<double> v = curve[i]-curve[i-1];
		v = v.get_unit_vector();
		u = v.get_perpendicular()[0];
		u = u*HALF_WIDTH;
		curve_left.push_back(p+u);
	}
	return curve_left;
}


// Takes a vector of points, our central curve, and creates the right part.
vector<point<double>> produce_right(const vector<point<double>>& curve) {
	vector<point<double>> curve_right;

	// Initialize & add the first one.
	point<double> start = curve[0]; start.x += HALF_WIDTH;
	curve_right.push_back(start);
	
	// Iterate through.
	point<double> u;
	for (int i=1; i<curve.size(); ++i) {
		// These are slightly harder to understand. Explanation in PDF.
		point<double> p = curve[i];
		point<double> v = curve[i]-curve[i-1];
		v = v.get_unit_vector();
		u = v.get_perpendicular()[1];
		u = u*HALF_WIDTH;
		curve_right.push_back(p+u);
	}
	return curve_right;
}
