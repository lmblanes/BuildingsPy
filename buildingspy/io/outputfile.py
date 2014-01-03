#!/usr/bin/env python
from buildingspy.thirdParty.dymat.DyMat import DyMatFile

class Reader:
    """Open the file *fileName* and parse its content.

    :param fileName: The name of the file.
    :param simulator: The file format. Currently, the only supported 
                   value is ``dymola``.

    This class reads ``*.mat`` files that were generated by Dymola
    or OpenModelica.

    """

    def __init__(self, fileName, simulator):
        if simulator != "dymola":
            raise ValueError('Argument "simulator" needs to be set to "dymola".')

        self.fileName = fileName
        self.__data__ = DyMatFile(fileName)

    def varNames(self, pattern=None):
        '''
           :pattern: A regular expression that will be used to filter the variable names.

           Scan through all variable names and return the variables 
           for which ``pattern``, as a regular expression, produces a match.
           If ``pattern`` is unspecified, all variable names are returned.

           This method searches the variable names using the **search** function
           from `Python's re module <http://docs.python.org/library/re.html>`_.

           See also http://docs.python.org/howto/regex.html#regex-howto.

           Usage: Type

              >>> import os
              >>> from buildingspy.io.outputfile import Reader
              >>> resultFile = os.path.join("buildingspy", "examples", "dymola", "PlotDemo.mat")
              >>> r=Reader(resultFile, "dymola")
              >>> # Return a list with all variable names
              >>> r.varNames() #doctest: +ELLIPSIS
              [u'PID.I.y_start', u'PID.Td', u'PID.I.der(y)', ...]
              >>> # Return ['const.k', 'const.y']
              >>> r.varNames('const')  
              [u'const.k', u'const.y']
              >>> # Returns all variables whose last character is u
              >>> r.varNames('u$')
              [u'PID.gainPID.u', u'PID.limiter.u', u'PID.gainTrack.u', u'PID.P.u', u'PID.I.u', u'gain.u']

        '''
        import re

        AllNames = self.__data__.names()
        if pattern is None:
            return AllNames
        else:
            AllNamesFilt=[]    # Filtered variable names
            for item in AllNames:
                if re.search(pattern, item):
                    AllNamesFilt.append(item)
            return AllNamesFilt         
            
     
    def values(self, varName):
        '''Get the time and data series.

        :param varName: The name of the variable.
        :return: An array where the first column is time and the second
                 column is the data series.

        Usage: Type
           >>> import os
           >>> from buildingspy.io.outputfile import Reader
           >>> resultFile = os.path.join("buildingspy", "examples", "dymola", "PlotDemo.mat")
           >>> r=Reader(resultFile, "dymola")
           >>> (time, heatFlow) = r.values('preHea.port.Q_flow')
        '''
        d = self.__data__.data(varName)
        a = self.__data__.abscissa(blockOrName=varName, valuesOnly=True)
        return a, d
    
    def integral(self, varName):
        '''Get the integral of the data series.

        :param varName: The name of the variable.
        :return: The integral of ``varName``.

        This function returns :math:`\int_{t_0}^{t_1} x(s) \, ds`, where
        :math:`t_0` is the start time and :math:`t_1` the final time of the data
        series :math:`x(\cdot)`, and :math:`x(\cdot)` are the data values
        of the variable ``varName``.
          
        
        Usage: Type
           >>> import os
           >>> from buildingspy.io.outputfile import Reader
           >>> resultFile = os.path.join("buildingspy", "examples", "dymola", "PlotDemo.mat")
           >>> r=Reader(resultFile, "dymola")
           >>> r.integral('preHea.port.Q_flow')
           -21.589191160164773
        '''
        (t, v)=self.values(varName)
        val=0.0;
        for i in range(len(t)-1):
            val = val + (t[i+1]-t[i]) * (v[i+1]+v[i])/2.0
        return val

    def mean(self, varName):
        '''Get the mean of the data series.

        :param varName: The name of the variable.
        :return: The mean value of ``varName``.

        This function returns 

        .. math::
           
           \\frac{1}{t_1-t_0} \, \int_{t_0}^{t_1} x(s) \, ds, 
         
        where :math:`t_0` is the start time and :math:`t_1` the final time of the data
        series :math:`x(\cdot)`, and :math:`x(\cdot)` are the data values
        of the variable ``varName``.
          
        
        Usage: Type
           >>> import os
           >>> from buildingspy.io.outputfile import Reader
           >>> resultFile = os.path.join("buildingspy", "examples", "dymola", "PlotDemo.mat")
           >>> r=Reader(resultFile, "dymola")
           >>> r.mean('preHea.port.Q_flow')
           -21.589191160164773
        '''
        t=self.values(varName)[0]
        r = self.integral(varName)/(max(t)-min(t))
        return r

    def min(self, varName):
        '''Get the minimum of the data series.

        :param varName: The name of the variable.
        :return: The minimum value of ``varName``.

        This function returns :math:`\min \{x_k\}_{k=0}^{N-1}`, where
        :math:`\{x_k\}_{k=0}^{N-1}` are the values of the variable ``varName``
        
        Usage: Type
           >>> import os
           >>> from buildingspy.io.outputfile import Reader
           >>> resultFile = os.path.join("buildingspy", "examples", "dymola", "PlotDemo.mat")
           >>> r=Reader(resultFile, "dymola")
           >>> r.min('preHea.port.Q_flow')
           -50.0
        '''
        v=self.values(varName)[1]
        return min(v)

    def max(self, varName):
        '''Get the maximum of the data series.

        :param varName: The name of the variable.
        :return: The maximum value of ``varName``.

        This function returns :math:`\max \{x_k\}_{k=0}^{N-1}`, where
        :math:`\{x_k\}_{k=0}^{N-1}` are the values of the variable ``varName``.
        
        Usage: Type
           >>> import os
           >>> from buildingspy.io.outputfile import Reader
           >>> resultFile = os.path.join("buildingspy", "examples", "dymola", "PlotDemo.mat")
           >>> r=Reader(resultFile, "dymola")
           >>> r.max('preHea.port.Q_flow')
           -11.284342
        '''
        v=self.values(varName)[1]
        return max(v)
