import numpy as np

class PIDController:
    def __init__(self, Kp=0.0, Ki=0.0, Kd=0.0, setpoint=0.0, dt = 0.0):
        """
        Initializes a PID controller object.

        Args:
            Kp (float): Proportional gain.
            Ki (float): Integral gain.
            Kd (float): Derivative gain.
            setpoint (float, optional): Desired setpoint value.
            dt (float): PID sampling time
        """

        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.dt = dt

        self.P = 0.0
        self.I = 0.0
        self.D = 0.0
        self.last_error = 0.0
        self.error = 0.0
        self.output = 0.0

    def update_parameters(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def update_output(self, setpoint, current_value):
        """
        Calculates the PID output based on the current value.

        Args:
            current_value (float): The current measured value.

        Returns:
            float: The calculated PID output.
        """
        self.setpoint = setpoint
        self.error = self.setpoint - current_value

        self.P = self.Kp * self.error
        self.I += self.Kp*self.Ki*(self.error + self.last_error)/2 * self.dt
        self.D = self.Kp*self.Kd*(self.error - self.last_error) / self.dt
        self.output = self.P + self.I + self.D

        self.last_error = self.error

        return np.array([self.output])