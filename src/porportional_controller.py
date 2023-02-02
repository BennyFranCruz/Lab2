class PorportionalController:   
    
    def __init__(self, Kp, initial_setpoint):
        
        self.Kp = Kp
        self.setpoint = initial_setpoint
        
    def run(self, setpoint, position):
        
        self.p_control_out = self.Kp*(setpoint - position)
        
        return self.p_control_out
    
        
if __name__ == "__main__":
    controller = PorportionalController(1, 1)
    
    #print(controller.run(1, .5))