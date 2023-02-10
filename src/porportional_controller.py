class PorportionalController:   
    
    def __init__(self, Kp):
        
        self.Kp = Kp
        
    def run(self, setpoint, currentposition):
        
        self.p_control_out = -self.Kp*(setpoint - currentposition)
        
        if self.p_control_out > 100:
            self.p_control_out = 100
        elif self.p_control_out <-100:
            self.p_control_out = -100
        
        return(self.p_control_out)
    
