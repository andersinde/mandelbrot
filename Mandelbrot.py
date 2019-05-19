import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from numba import jit

# this function is outside of the class so that we can use jit
@jit
def _determineDivergence(cr, ci, maxIter, horizon2, log_horizon):
	"""returns number of iterations until loop break for a given
	 complex number c = cr + i*ci"""

	(zr, zi) = (cr, ci) # z after first iteration
	for n in range(maxIter):
		zr2 = zr*zr
		zi2 = zi*zi
		if zr2 + zi2 > horizon2:
			return n + 1 - np.log(np.log(zr2 + zi2))/0.602 + log_horizon
		zi = 2*zr*zi + ci
		zr = zr2 - zi2 + cr
	return 0

class Mandelbrot:
	"""A class representing an object used for customizing and plotting the mandelbrot set"""

	def __init__(self, width=9, height=6, dpi=72, extent=[-2,1,-1,1], maxIter=128, cmap="cubehelix", zoom=2):

		self.width = width
		self.height = height
		self.dpi = dpi

		self.extent = extent
		self.maxIter = maxIter
		self.cmap = cmap
		self.zoom = zoom
		self._start = True

	def getMandelbrotSet(self):
		"""Performs _isInMandelbrotSet on every pixel and returns the result in an array"""
		
		(x_min, x_max, y_min, y_max) = [i for i in self.extent]
		(rows, columns) = (self.width*self.dpi, self.width*self.dpi)
		r_real = np.linspace(x_min, x_max, columns)
		r_imag = np.linspace(y_max, y_min, rows)
		result = np.empty((rows, columns))

		# used for smoother colors
		horizon = 2.0**40
		horizon2 = horizon**2
		log_horizon = np.log(np.log(horizon))/np.log(2)

		for i in range(rows): # imaginary values
			for j in range(columns): # real values
				result[i,j] = _determineDivergence(r_real[j], r_imag[i], self.maxIter, horizon2, log_horizon)
		return result

	def _handleClick(self, event):
		""""zoom in and update image when clicking on figure"""

		(x_min, x_max, y_min, y_max) = [i for i in self.extent]
		if event.xdata != None and event.ydata != None:
			(click_x, click_y) = (event.xdata, event.ydata)
			newWidth = (x_max-x_min)/self.zoom
			newHeight = (y_max-y_min)/self.zoom

			# update self.extent to the new zoomed in extent
			self.extent = [click_x-newWidth/2, click_x+newWidth/2, click_y-newHeight/2, click_y+newHeight/2]
			self.plot()

	def plot(self):
		"""Plot using matplotlib"""

		mandelbrotSet = self.getMandelbrotSet()

		if self._start: # the first time this method is called, setup the figure
			self._start = False

			fig, ax = plt.subplots(figsize=(self.width, self.height))
			fig.canvas.mpl_connect('button_press_event', self._handleClick) # connect zoom interaction

			norm = colors.PowerNorm(0.3)
			plt.imshow(mandelbrotSet, extent=self.extent, interpolation="nearest", cmap=self.cmap, norm=norm)
			plt.title("Click where you want to zoom in")
			return plt.show()

		else: # just redraw the image
			norm = colors.PowerNorm(0.3)
			plt.imshow(mandelbrotSet, extent=self.extent, interpolation="nearest", cmap=self.cmap, norm=norm)
			plt.draw()

if __name__ == "__main__":
	# example usage
	
	extent = [-2,1,-1,1] # full size
	# extent = [-0.35,0.08,0.63,1]
	# extent = [-0.1443,-0.1432,-0.8389,-0.8379]

	mandel = Mandelbrot(extent=extent, dpi=128, maxIter=400, cmap="gnuplot2", zoom=5)
	mandel.plot()
