/*

This file simulates the curve creation.

*/


#include "arrow_curve.h"


using namespace std;


void add_point_straight(vector<point<double>>& straight_line) {
	point<double> p0(0.0, 0.0); straight_line.push_back(p0);
	point<double> p1(0.0, 1.0); straight_line.push_back(p1);
	point<double> p2(0.0, 2.0); straight_line.push_back(p2);
	point<double> p3(0.0, 3.0); straight_line.push_back(p3);
	point<double> p4(0.0, 4.0); straight_line.push_back(p4);
	point<double> p5(0.0, 5.0); straight_line.push_back(p5);
	point<double> p6(0.0, 6.0); straight_line.push_back(p6);
}


void add_point_curved(vector<point<double>>& curved_line) {
	point<double> p0(0.0, 0.0); curved_line.push_back(p0);
	point<double> p1(0.0, 1.0); curved_line.push_back(p1);
	point<double> p2(1.0, 2.0); curved_line.push_back(p2);
	point<double> p3(0.0, 3.0); curved_line.push_back(p3);
	point<double> p4(-1.0, 4.0); curved_line.push_back(p4);
	point<double> p5(0.0, 5.0); curved_line.push_back(p5);
	point<double> p6(1.0, 6.0); curved_line.push_back(p6);
}


template <typename T>
void print_vector(vector<T> list) {
	for (auto element : list) cout << element << endl;
}


void test() {
	point<double> v(-3.0, 4.0);
	v = v.get_unit_vector();
	vector<point<double>> u_choices = v.get_perpendicular();
	point<double> u1 = u_choices[0], u2 = u_choices[1];
	cout << u1 << endl;
	cout << u2 << endl;
}


// Demonstrates the usage of this program.
// - Input: a small number (n) of zig-zag points that denote the ideal arrow tracing.
// - Output: a curve for the arrow, containing DIV_PARAMETER * n of "point" instances.
void run() {
	// Create the vectors of points first.
	vector<point<double>> straight_line, raw_curved_line;

	// Add points to them.
	add_point_straight(straight_line);
	add_point_curved(raw_curved_line);

	// Make the "trans" vector of points (modified from raw to perform "bezier").
	vector<point<double>> trans = transform_raw_points(raw_curved_line);

	// Produce the curve.
	vector<point<double>> curve = produce_curve(trans);
	vector<point<double>> curve_left = produce_left(curve);
	vector<point<double>> curve_right = produce_right(curve);

	// Prints the curve.
	print_vector(curve);
	print_vector(curve_left);
	print_vector(curve_right);
}


int main() {
	run();
}
