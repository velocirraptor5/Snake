import numpy as np

class RedNeuronal:
    def __init__(self,neu,eta,p=[[[-1]]]):
        self.neu=neu
        self.eta=eta
        self.p=p
        self.S=[-1,-1,-1,-1]

    def _nonlin_(self,x,deriv=False):
      if(deriv==True):
          return x*(1-x)
      return 1/(1+np.exp(-x))
    
    def _lin_(self,x,deriv=False):
        if(deriv==True):
            return 1
        return x

    def _iniciarPesos_(self,entrada):
        #np.random.seed(1)
        try:
            if(self.p[0][0][0]==-1):
                self.p[0] = 2*np.random.rand(len(entrada),self.neu) - 1  
                self.p.append(2*np.random.rand(self.neu,self.neu) - 1)
                self.p.append(2*np.random.rand(self.neu,4) - 1)
        except:
            return

    def probar(self,entrada):
        self._iniciarPesos_(entrada)
        
        self.S[0]=np.array(entrada)
        neta1=np.dot(self.S[0],self.p[0])

        self.S[1]=self._nonlin_(neta1)
        neta2=np.dot(self.S[1],self.p[1])

        self.S[2]=self._nonlin_(neta2)
        neta3=np.dot(self.S[2],self.p[2])

        self.S[3]=self._nonlin_(neta3)
        return self.S[3]

    def entrenar(self,error):
        S3_error=error
        S3_delta=np.array(S3_error*self._nonlin_(self.S[3],True)*self.eta)[np.newaxis]
        
        S2_error=S3_delta.dot(self.p[2].T)
        S2_delta=S2_error*self._nonlin_(self.S[2],True)*self.eta

        S1_error=S2_error.dot(self.p[1].T)
        S1_delta=S1_error*self._nonlin_(self.S[1],True)*self.eta


        
        S2T=(np.array(self.S[2])[np.newaxis]).T
        S1T=(np.array(self.S[1])[np.newaxis]).T
        S0T=(np.array(self.S[0])[np.newaxis]).T


        self.p[2] += S2T.dot(S3_delta)
        self.p[1] += np.dot(S1T,S2_delta)
        self.p[0] += np.dot(S0T,S1_delta)
    
        


