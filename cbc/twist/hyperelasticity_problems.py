__author__ = "Harish Narayanan"
__copyright__ = "Copyright (C) 2009 Simula Research Laboratory and %s" % __author__
__license__  = "GNU GPL Version 3 or any later version"

from dolfin import *
from cbc.common import CBCProblem
from cbc.twist.equation_solvers import StaticMomentumBalanceSolver, MomentumBalanceSolver

class StaticHyperelasticityProblem(CBCProblem):
    """Base class for all static hyperelasticity problems"""

    def __init__(self):
        """Create the static hyperelasticity problem"""
        pass

    def solve(self):
        """Solve for and return the computed displacement field, u"""
        solver = StaticMomentumBalanceSolver()
        return solver.solve(self)

    def body_force(self, vector):
        """Return body force, B"""
        B = Constant(vector.mesh(), (0,)*vector.mesh().geometry().dim())
        return B

    def surface_force(self, vector):
        """Return the surface tractions, T"""
        T = Constant(vector.mesh(), (0,)*vector.mesh().geometry().dim())
        return T

    def material_model(self):
        pass

    def first_pk_stress(self, u):
        """Return the first Piola-Kirchhoff stress tensor, P, given a
        displacement field, u"""
        return self.material_model().FirstPiolaKirchhoffStress(u)

    def second_pk_stress(self, u):
        """Return the second Piola-Kirchhoff stress tensor, S, given a
        displacement field, u"""
        return self.material_model().SecondPiolaKirchhoffStress(u)

    def boundary_conditions(self, vector):
        """"Return Dirichlet boundary conditions for the displacment
        field"""
        return []

    def functional(self, u):
        """Return value of goal functional"""
        return None

    def reference(self):
        """"Return reference value for the goal functional"""
        return None

    def __str__(self):
        """Return a short description of the problem"""
        return "Static hyperelasticity problem"

class HyperelasticityProblem(StaticHyperelasticityProblem):
    """Base class for all quasistatic/dynamic hyperelasticity
    problems"""

    def __init__(self):
        """Create the hyperelasticity problem"""
        pass

    def solve(self):
        """Solve for and return the computed displacement field, u"""
        solver = MomentumBalanceSolver()
        return solver.solve(self)

    def end_time(self):
        """Return the end time of the computation"""
        pass

    def time_step(self):
        """Return the time step size"""
        pass

    def is_dynamic(self):
        """Return True if the inertia term is to be considered, or
        False if it is to be neglected (quasi-static)"""
        pass

    def reference_density(self, scalar):
        """Return the reference density of the material"""
        rho0 = Constant(scalar.mesh(), 1.0)
        return rho0        

    def initial_conditions(self, vector):
        """Return initial conditions for displacement field, u0, and
        velocity field, v0""" 
        u0 = Constant(vector.mesh(), (0,)*vector.mesh().geometry().dim())
        v0 = Constant(vector.mesh(), (0,)*vector.mesh().geometry().dim())
        return u0, v0

    def body_force(self, t, vector):
        """Return body force, B, at time t"""
        B = Constant(vector.mesh(), (0,)*vector.mesh().geometry().dim())
        return B

    def surface_force(self, t, vector):
        """Return the surface tractions, T, at time t"""
        T = Constant(vector.mesh(), (0,)*vector.mesh().geometry().dim())
        return T

    def boundary_conditions(self, t, vector):
        """"Return Dirichlet boundary conditions for the displacment
        field, u, at time t"""
        return []