/*

This file stores the point class.

*/


#include <iostream>
#include <vector>
#include <cmath>


using namespace std;


// A class for 2-dimensional vectors.
template <typename T>
class point {
public:
	T x; T y;

	point() {
	}

	point(T x_input, T y_input): x{x_input}, y{y_input} {
	}

    point(const point<T>& other) : x{ other.x }, y{ other.y } {
    }

    point<T>& operator=(const point<T>& other) {
        if (this != &other) {
            x = other.x;
            y = other.y;
        }
        return *this;
    }

	void set_coordinates(T x_input, T y_input) {
		x = x_input; y = y_input;
	}

	point<T> get_unit_vector() {
		T magnitude = sqrt(x * x + y * y);
		point<T> unit_v(x / magnitude, y / magnitude);
		return unit_v;
	}

	vector<point<T>> get_perpendicular() {
		point<T> va, vb, vc;
		vector<point<T>> output;
		T k_squared = x*x + y*y;

		if (y==0) {
			va.x = 0; va.y = x; vb.x = 0; vb.y = -x;
		}
		else if (x==0) {
			va.x = y; va.y = 0; vb.x = -y; vb.y = -0;
		}
		else {
			T r = (-x)/y; // We get ratio r = (-x)/y = py/px.
			T nx = sqrt(k_squared / (r*r+1)); T ny = sqrt(k_squared - nx*nx);

			if (nx*x*ny*y > 0) {
				va.x = nx; va.y = -ny; vb.x = -nx; vb.y = ny;
			}
			else {
				va.x = nx; va.y = ny; vb.x = -nx; vb.y = -ny;
			}
		}

		if (va.x > x) { // Swap if necessary, to allow sorting by x values.
			vc = va; va = vb; vb = vc;
		}

		output.push_back(va); output.push_back(vb);

		return output;
	}
};


// Defining scalar multiplication LHS.
template <typename T>
point<T> operator*(T c, const point<T>& v) {
	point<T> v_product(c * v.x, c * v.y);
	return v_product;
}


// Defining scalar multiplication RHS.
template <typename T>
point<T> operator*(const point<T>& v, T c) {
	point<T> v_product(c * v.x, c * v.y);
	return v_product;
}


// Defining vector addition.
template <typename T>
point<T> operator+(const point<T>& left, const point<T>& right) {
	point<T> v_sum(left.x + right.x, left.y + right.y);
	return v_sum;
}


// Defining vector subtraction.
template <typename T>
point<T> operator-(const point<T>& left, const point<T>& right) {
	point<T> v_difference(left.x - right.x, left.y - right.y);
	return v_difference;
}


// Defining the dot product.
template <typename T>
T operator*(const point<T>& left, const point<T>& right) {
	return left.x*right.x + left.y*right.y;
}


// Defining coordinate printing.
template <typename T>
std::ostream& operator<<(std::ostream& out, const point<T>& v) {
	out << "(" << v.x << ", " << v.y << ")";
	return out;
}
