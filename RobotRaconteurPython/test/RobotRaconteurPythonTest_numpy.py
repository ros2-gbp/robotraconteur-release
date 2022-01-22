import sys
import time
from os import path
import struct
import threading
import thread
import os
import traceback
import numpy

#sys.path.append(r"C:\Users\wasonj\Documents\RobotRaconteur2\bin\out\Python")

from RobotRaconteur import *

def MultiDimArrayToNumPy(array,dtype=None):
    if (dtype==None): dtype=numpy.float64
    if (array.Complex):
        if (dtype!=numpy.complex64 and dtype!=numpy.complex128):
            return (numpy.array(array.Real,dtype).reshape(array.Dims),numpy.array(array.Imag,dtype).reshape(array.Dims))
        else:
            return numpy.array(array.Real,dtype).reshape(array.Dims) + 1j*numpy.array(array.Imag,dtype).reshape(array.Dims)
    else:
        return numpy.array(array.Real,dtype).reshape(array.Dims)

def NumPyToMultiDimArray(narray):
    if (type(narray) is list or type(narray) is set or type(narray) is tuple):
        dims=narray[0].shape
        real=list(narray[0].flatten(order="F"))
        imag=list(narray[1].flatten(order="F"))
        return MultiDimArray(dims,real,imag)
    else:
        if (dtype!=numpy.complex64 and dtype!=numpy.complex128):
            dims=narray.shape
            real=list(narray.flatten(order="F"))

            return MultiDimArray(dims,real,None)
        else:
            dims=narray.shape
            real=list(narray.real.flatten(order="F"))
            imag=list(narray.imag.flatten(order="F"))
            return MultiDimArray(dims,real,imag)



class MultiDimArrayTest(object):

    TestDataPath="."

    @staticmethod
    def Test():
        MultiDimArrayTest.TestDouble()
        MultiDimArrayTest.TestByte()


    @staticmethod
    def TestDouble():
        m1 = MultiDimArrayTest.LoadDoubleArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray1.bin"))
        m2 = MultiDimArrayTest.LoadDoubleArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray2.bin"))
        m3 = MultiDimArrayTest.LoadDoubleArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray3.bin"))
        m4 = MultiDimArrayTest.LoadDoubleArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray4.bin"))
        m5 = MultiDimArrayTest.LoadDoubleArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray5.bin"))
        m1.AssignSubArray([2, 2, 3, 3, 4], m2, [0, 2, 0, 0, 0], [1, 5, 5, 2, 1])
        ca(m1.Real, m3.Real)
        ca(m1.Imag, m3.Imag)
        m6 = MultiDimArray([2, 2, 1, 1, 10], [0]*40, [0]*40)
        m1.RetrieveSubArray([4, 2, 2, 8, 0], m6, [0, 0, 0, 0, 0], [2, 2, 1, 1, 10])
        ca(m4.Real, m6.Real)
        ca(m4.Imag, m6.Imag)
        m7 = MultiDimArray([4, 4, 4, 4, 10], [0]*2560, [0]*2560)
        m1.RetrieveSubArray([4, 2, 2, 8, 0], m7, [2, 1, 2, 1, 0], [2, 2, 1, 1, 10])
        ca(m5.Real, m7.Real)
        ca(m5.Imag, m7.Imag)



    @staticmethod
    def TestByte():
        m1 = MultiDimArrayTest.LoadByteArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray_b1.bin"))
        m2 = MultiDimArrayTest.LoadByteArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray_b2.bin"))
        m3 = MultiDimArrayTest.LoadByteArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray_b3.bin"))
        m4 = MultiDimArrayTest.LoadByteArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray_b4.bin"))
        m5 = MultiDimArrayTest.LoadByteArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray_b5.bin"))
        m1.AssignSubArray([50, 100], m2, [20, 25], [200, 200])
        ca(m1.Real, m3.Real)
        m6 = MultiDimArray([200, 200], [0]*40000)
        m1.RetrieveSubArray([65, 800], m6, [0, 0], [200, 200])
        ca(m4.Real, m6.Real)
        m7 = MultiDimArray([512, 512], [0]*(512 * 512))
        m1.RetrieveSubArray([65, 800], m7, [100, 230], [200, 200])
        ca(m5.Real, m7.Real)




    @staticmethod
    def LoadDoubleArrayFromFile(fname):
        f =open(fname,'rb')
        a = MultiDimArrayTest.LoadDoubleArray(f)
        f.close()
        return a


    @staticmethod
    def LoadDoubleArray(s):
        r = MultiDimArrayTest.BinaryReader(s)
        dimcount = r.ReadInt32()
        dims = [0]*dimcount
        count = 1
        i = 0
        while i < dimcount:
            dims[i] = r.ReadInt32()
            count *= dims[i]
            i += 1
        real = [0]*count
        i = 0
        while i < count:
            real[i] = r.ReadDouble()
            i += 1
        if (r.Available()) > 0:
            imag = [0]*count
            i = 0
            while i < count:
                imag[i] = r.ReadDouble()
                i += 1
            return MultiDimArray(dims, real, imag)
        else:
            return MultiDimArray(dims, real)


    @staticmethod
    def LoadByteArrayFromFile(fname):
        f = open(fname,'rb')
        a = MultiDimArrayTest.LoadByteArray(f)
        f.close()
        return a



    @staticmethod
    def LoadByteArray(s):
        r = MultiDimArrayTest.BinaryReader(s)
        dimcount = r.ReadInt32()
        dims = [0]*dimcount
        count = 1
        i = 0
        while i < dimcount:
            dims[i] = r.ReadInt32()
            count *= dims[i]
            i += 1
        real = [0]*count
        i = 0
        while i < count:
            real[i] = r.ReadByte()
            i += 1
        if (r.Available()) > 0:
            imag = [0]*count
            i = 0
            while i < count:
                imag[i] = r.ReadByte()
                i += 1
            return MultiDimArray(dims, real, imag)
        else:
            return MultiDimArray(dims, real)

    class BinaryReader(object):
        def __init__(self,f):
            self.f=f

        def ReadByte(self):
            dat=self.f.read(1)
            return struct.unpack("<B",dat)[0]

        def ReadInt32(self):
            dat=self.f.read(4)
            return struct.unpack("<i",dat)[0]

        def ReadDouble(self):
            dat=self.f.read(8)
            return struct.unpack("<d",dat)[0]

        def Available(self):
            s=os.fstat(self.f.fileno()).st_size
            return s-self.f.tell()



RobotRaconteurTestService_robdef="""
#This is the standard test service for RobotRaconteur
#It is not meant to be exhaustive, rather it tests the
#most common operations.

#Each of the members defined has a specified behavior.
#Refer to the reference implementation for details
#on these behaviors.  New implementations of
#Robot Raconteur should test against the reference
#client and server to determine compatibilty.

service RobotRaconteurTestService

option version1 0.2.0.5

import RobotRaconteurTestService2

struct teststruct1
    field double[] dat1
    field string str2
    field string{int32} vec3
    field string{string} dict4
    field string{list} list5
    field teststruct2 struct1
    field teststruct2{string} dstruct2
    field teststruct2{list} lstruct3
    field double[*] multidimarray

    field varvalue var3

end struct

struct teststruct2
    field double[] mydat

end struct

object testroot
    implements RobotRaconteurTestService2.baseobj

    option constant double[] doubleconst {3.4, 4.8, 14372.8}
    option constant string strconst "This is a constant"

#Properties to test the serialization of different data types

    #numbers

    property double d1
    property double[] d2
    property double[16] d3
    property double[16-] d4
    property double[*] d5
    property double[3,3] d6

    property single s1
    property single[] s2

    property int8 i8_1
    property int8[] i8_2

    property uint8 u8_1
    property uint8[] u8_2
    property uint8[*] u8_3

    property int16 i16_1
    property int16[] i16_2

    property uint16 u16_1
    property uint16[] u16_2

    property int32 i32_1
    property int32[] i32_2

    property uint32 u32_1
    property uint32[] u32_2

    property int64 i64_1
    property int64[] i64_2

    property uint64 u64_1
    property uint64[] u64_2

    #strings
    property string str1

    #structs
    property teststruct1 struct1
    property teststruct2 struct2

    #indexed sets
    property double{int32} is_d1
    property double{string} is_d2
    property double[]{int32} is_d3
    property double[]{string} is_d4
    property double[*]{int32} is_d5
    property double[*]{string} is_d6

    property string{int32} is_str1
    property string{string} is_str2

    property teststruct2{int32} is_struct1
    property teststruct2{string} is_struct2
    property RobotRaconteurTestService2.ostruct2 struct3

    #lists
    property double{list} list_d1
    property double[]{list} list_d3
    property double[*]{list} list_d5

    property string{list} list_str1
    property teststruct2{list} list_struct1

    #varvalue
    property varvalue var1
    property varvalue{int32} var2
    property varvalue var_num
    property varvalue var_str
    property varvalue var_struct
    property varvalue var_vector
    property varvalue var_dictionary
    property varvalue var_multidimarray

    #Throw an error to test error transmission
    property double errtest
    property teststruct1 nulltest

    #functions
    function void func1()
    function void func2(double d1, double d2)
    function double func3(double d1, double d2)
    function int32 meaning_of_life()
    function void func_errtest()

    #events

    event ev1()
    event ev2(double d1, teststruct2 s2 )

    #objrefs

    objref sub1 o1
    objref sub1[] o2
    objref sub1{int32} o3
    objref sub1{string} o4
    objref RobotRaconteurTestService2.subobj o5

    objref varobject o6

    function void o6_op(int32 op)

    #pipes

    pipe double[] p1

    #option pipe p2 unreliable
    pipe teststruct2 p2
    function void pipe_check_error()

    #callbacks
    callback void cb1()
    callback void cb2(double d1, double d2)
    callback double cb3(double d1, double d2)
    callback int32 cb_meaning_of_life()
    callback void cb_errtest()

    function void test_callbacks()

    #wires

    wire double[] w1
    wire teststruct2 w2
    wire int32[*] w3

    #memory

    memory double[] m1
    memory double[*] m2
    memory uint8[*] m3

end object

object sub1
    property double[] d1
    property double[*] d2

    objref sub2 o2_1
    objref sub2{int32} o2_2
    objref sub2{string} o2_3

    property string s_ind
    property int32 i_ind

end object

object sub2

    property string s_ind
    property int32 i_ind

    property string data
    objref sub3{string} o3_1
end object

object sub3
    property string ind
    property string data2
    property double data3
    function double add(double d)
end object
"""

RobotRaconteurTestService2_robdef="""
service RobotRaconteurTestService2

struct ostruct2
    field double[] a1
end struct


object baseobj
    property double d1
    property double[] d2

    function double func3(double d1, double d2)

    event ev1()

    objref subobj o5

    pipe double[] p1

    callback void cb2(double d1, double d2)

    wire double[] w1

    memory double[] m1


end object

object subobj

    function double add_val(double v)

end object
"""

def main():

    MultiDimArrayTest.TestDataPath=os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "testing" ,"testdata")
    RobotRaconteurNode.s.UseNumPy=True
    if (len(sys.argv)>1):
        command=sys.argv[1]
    else:
        command="loopback"

    if (command=="loopback"):
        t=TcpTransport()
        t.EnableNodeAnnounce(IPNodeDiscoveryFlags_NODE_LOCAL | IPNodeDiscoveryFlags_LINK_LOCAL | IPNodeDiscoveryFlags_SITE_LOCAL)
        t.EnableNodeDiscoveryListening(IPNodeDiscoveryFlags_NODE_LOCAL | IPNodeDiscoveryFlags_LINK_LOCAL | IPNodeDiscoveryFlags_SITE_LOCAL)
        t.StartServer(4564)

        RobotRaconteurNode.s.RegisterServiceType(RobotRaconteurTestService2_robdef)
        RobotRaconteurNode.s.RegisterServiceType(RobotRaconteurTestService_robdef)

        RobotRaconteurNode.s.RegisterTransport(t)

        t=testroot_impl()
        context=RobotRaconteurNode.s.RegisterService("RobotRaconteurTestService","RobotRaconteurTestService.testroot",t)
        def scallback(context,code,param):
            print "Server callback " + str(code) + " " + str(param)
        context.AddServerServiceListener(scallback)

        t2=testroot_impl()
        authdata="testuser1 0b91dec4fe98266a03b136b59219d0d6 objectlock\ntestuser2 841c4221c2e7e0cefbc0392a35222512 objectlock\ntestsuperuser 503ed776c50169f681ad7bbc14198b68 objectlock,objectlockoverride"
        p=PasswordFileUserAuthenticator(authdata)
        policies={"requirevaliduser" : "true", "allowobjectlock" : "true"}
        s=ServiceSecurityPolicy(p,policies)

        RobotRaconteurNode.s.RegisterService("RobotRaconteurTestService_auth","RobotRaconteurTestService.testroot",t2,s)

        s=ServiceTestClient();
        s.RunFullTest('rr+tcp://localhost:4564/?service=RobotRaconteurTestService','rr+tcp://localhost:4564/?service=RobotRaconteurTestService_auth')


        RobotRaconteurNode.s.Shutdown()

        print "Test completed no errors detected"

        return

    if (command=="client"):
        url1=sys.argv[2]
        url2=sys.argv[3]

        t=TcpTransport()
        t.EnableNodeDiscoveryListening(IPNodeDiscoveryFlags_NODE_LOCAL | IPNodeDiscoveryFlags_LINK_LOCAL | IPNodeDiscoveryFlags_SITE_LOCAL)

        RobotRaconteurNode.s.RegisterTransport(t)

        s=ServiceTestClient();
        s.RunFullTest(url1,url2)

        RobotRaconteurNode.s.Shutdown()

        print "Test completed no errors detected"
        return

    if (command=="server"):

        #MultiDimArrayTest.Test()
        port=int(sys.argv[2])
        id=NodeID(sys.argv[3])
        nodename=(sys.argv[4])

        RobotRaconteurNode.s.NodeID=id
        RobotRaconteurNode.s.NodeName=nodename

        RobotRaconteurNode.s.RegisterServiceType(RobotRaconteurTestService_robdef)
        RobotRaconteurNode.s.RegisterServiceType(RobotRaconteurTestService2_robdef)

        t=TcpTransport()
        t.EnableNodeAnnounce(IPNodeDiscoveryFlags_NODE_LOCAL | IPNodeDiscoveryFlags_LINK_LOCAL | IPNodeDiscoveryFlags_SITE_LOCAL)
        t.StartServer(port)

        RobotRaconteurNode.s.RegisterTransport(t)

        t=testroot_impl()
        RobotRaconteurNode.s.RegisterService("RobotRaconteurTestService","RobotRaconteurTestService.testroot",t)

        t2=testroot_impl()
        authdata="testuser1 0b91dec4fe98266a03b136b59219d0d6 objectlock\ntestuser2 841c4221c2e7e0cefbc0392a35222512 objectlock\ntestsuperuser 503ed776c50169f681ad7bbc14198b68 objectlock,objectlockoverride"
        p=PasswordFileUserAuthenticator(authdata)
        policies={"requirevaliduser" : "true", "allowobjectlock" : "true"}
        s=ServiceSecurityPolicy(p,policies)

        RobotRaconteurNode.s.RegisterService("RobotRaconteurTestService_auth","RobotRaconteurTestService.testroot",t2,s)

        print "Server ready"
        raw_input("Press enter to quit")
        RobotRaconteurNode.s.Shutdown()
        return

    raise Exception("Unknown test command")

def ca(a,b):
    if (len(a) != len(b)): raise Exception()
    for i in range(len(a)):
        if (isinstance(a[i],float) and isinstance(b[i],float)):
            d=a[i]
            if (a[i]==0 and b[i]==0): return
            if abs((a[i]-b[i])/a[i])>.001:
                raise Exception()
        else:

            if (a[i] != b[i]):
                print a[i]
                print b[i]
                raise Exception()

class ServiceTestClient:
    def __init__(self):

        self._packetnum = 0
        self._ack_recv = False


    def RunFullTest(self, url, authurl):
        self.ConnectService(url)
        #self.TestProperties()
        """self.TestFunctions()
        self.TestEvents()
        self.TestObjRefs()
        self.TestPipes()
        self.TestCallbacks()
        self.TestWires()"""
        self.TestMemories()
        """self.DisconnectService()
        self.TestAuthentication(authurl)
        self.TestObjectLock(authurl)
        self.TestMonitorLock(url)"""



    def ConnectService(self, url):
        self._r = RobotRaconteurNode.s.ConnectService(url)
        attributes=RobotRaconteurNode.s.GetServiceAttributes(self._r)
        print attributes

    def DisconnectService(self):
        RobotRaconteurNode.s.DisconnectService(self._r)

    def TestProperties(self):
        self._r.d1 = 3.456
        if self._r.d1 != 12.345:
            raise Exception()
        self._r.d2 = numpy.array([8.805544e-12, 3.735066e+12, 3.491919e+17, 4.979833e+12, -4.042302e+00, 2.927731e-12, 5.945355e+11, -3.965351e+06, 4.866934e-14, 1.314597e+04, -2.059923e-11, -5.447989e-20, 1.267732e-21, -2.603983e+10, 2.417961e+03, 3.515469e-16, 1.731329e-01, -2.854408e-04, 2.908090e-06, 3.354746e+08, 9.405914e+05, -3.665276e-01, -2.036897e+02, 3.489765e-01, -3.207702e+11, -2.105708e+18, -1.485891e+13, -7.059704e+04, 3.528381e+11, 4.586056e+02, -8.107050e-16, -1.007106e+09, 2.964453e+05, -3.628810e+05, -2.816870e-14, 5.665387e+09, 8.518736e+11, -1.179981e+12, -1.506569e-21, 1.113076e-06, -4.782847e+06, 8.906463e+17, 2.729604e+03, -3.430604e+16, 2.626956e-07, 1.543395e+15, 3.407777e-21, 1.231519e+06, -4.808410e+16, 2.649811e+10, 2.546524e+01, -3.533472e-13, -3.732759e+04, 1.951505e-20, 9.338953e-21, -1.627672e-04, 1.807084e-19, -4.489206e-17, -2.654284e+08, -2.136947e+16, -3.690031e+09, 3.372245e-14, 4.946361e-11, -1.330965e-01, 2.479789e-17, 2.750331e-18, -4.301452e-03, 3.895091e+19, 2.515863e+13, 6.879298e+12, -2.925884e-15, -2.826248e+00, -4.864526e-06, 2.614765e+00, 4.488816e-19, 2.231337e+15, -7.004595e+07, 2.506835e-08, -2.187450e-02, -2.220025e-07, 1.688346e+02, 8.125250e-07, -4.819391e+10, -1.643306e-14, -4.768222e-18, -4.472162e-16, 2.487563e-01, -3.924904e-15, -1.186331e+06, 2.397369e+01, -3.137448e-02, 1.016507e+06, 2.584749e-16, 8.212180e-08, 1.631561e-12, -4.927066e-08, 1.448920e-14, -4.371505e+03, 2.050871e-21, 2.523287e+01, 7.778552e-05, -4.437786e+18, -1.118552e-07, -3.543717e-09, -5.327587e-07, -1.083197e-17, 2.578295e-10, -4.952430e-12, -3.008597e-13, 3.010829e+01, -6.109332e+09, -2.428341e-03, 9.399191e-01, -4.827230e-06, 1.013860e+10, -2.870341e-20, 4.281756e+11, 1.043519e-09, 2.378027e+06, 2.605309e+09, -4.939600e-04, -2.193966e+08, 4.022755e-03, 2.668705e-09, -1.087393e-18, 1.927676e-12, -1.694835e+10, 3.554035e-03, -1.299796e+01, -1.692862e+07, 2.818156e+07, -2.606821e-13, 1.629588e-15, -7.069991e-16, 1.205863e-19, 2.491209e-17, -3.757951e+04, 3.110266e-04, -4.339472e+11, -3.172428e+02, 1.579905e+09, 2.859499e-01, 4.241852e-06, 2.043341e-09, 2.922865e-16, -2.580974e+01, -3.147566e-02, 1.160590e+03, -2.238096e+01, -1.984601e-13, 2.636096e-03, 8.422872e-04, 2.026040e-16, -3.822500e+01, -2.190513e-18, 3.229839e-11, -2.958164e+06, -8.354021e+11, 3.625367e+08, -4.558085e-01, 1.274325e+04, -2.492750e+05, 3.739269e+18, -3.985407e-03, 3.575816e-13, 1.376847e+06, -6.682659e-20, -9.200014e+08, -2.278973e+10, -3.555184e-04, 3.821512e-10, 5.944167e+07, -2.576511e-15, 1.232459e+02, -3.187831e+02, -4.882568e+12, -1.670486e+05, -2.339878e-20, -4.985496e-16, -2.937093e+17, 8.981723e-06, -5.460686e-04, 1.090528e-11, -4.321598e+17, -3.577227e-08, 2.880194e+01, -4.277921e+00, -4.145678e-02, 4.930810e+08, -4.525745e-21, 4.648764e+07, -2.564920e+16, 1.075546e+01, 3.777591e-18, 1.419816e-08, 1.419490e+10, 1.479453e-19, -4.933130e+13, 4.580471e+15, -3.160785e+02, -2.885209e+06, 2.384424e-03, 1.030777e-12, 2.652784e+04, 4.435144e+10, 3.102484e+17, 4.725294e+11, -3.817788e-04, 4.074841e-01, -7.248042e-13, -4.502531e-08, 2.203521e+01, -4.457124e+01, -2.961745e+06, -3.237080e+14, -3.482497e-19, 1.534088e+05, 4.759060e-14, 2.333791e+04, -4.002051e-03, 3.278553e-06, -2.307217e+13, -2.999411e+19, -9.804484e+02, -1.793367e+01, 3.111735e+07, -4.457329e+10, -2.067659e-13, -5.927573e+03, 6.979879e+10, 3.556110e-06, -3.513094e-13, 1.128057e+19, 4.199038e+13, 7.553080e-20, 4.380028e-11, -2.502103e-19, 5.943049e+15, -1.266134e-10, 4.825578e-09, -2.778134e-16, 1.881866e-10, -3.677556e+08, -2.166345e-10, 3.919158e+05, 2.778912e-07, 1.822489e-05, 1.513496e-01, 9.327925e+05, -4.050132e-14, 3.311913e+01, 9.290544e+15, 1.302267e+03, -1.252080e+17, -4.208811e-04, -3.225464e+16, 2.093787e+16, -3.352116e+07, 4.797665e+15, -1.539672e-17, 4.835159e+04, 2.446236e-07, 2.355328e-17, 2.044244e-12, 3.210415e-11, -1.322741e+16, 5.538184e-14, -4.612046e-05, 4.758939e+15, -2.038208e-10, -2.451148e+18, -2.699711e-19, -2.019804e-09, 5.631634e-13, -2.288031e+05, -3.211488e+12, 7.511869e+13, -3.209453e-09, 3.806128e-18, 4.025006e-14, -1.700945e-10, 4.136280e-13, 4.517870e-04, 2.739233e+11, -3.736057e-03, 2.255379e-20, 3.122584e-16, 3.192660e-18, 4.765755e-09, 2.396494e-13, 1.625326e+02, -3.413821e-18, 3.627586e+10, 8.708108e+07, 2.244241e-09, 3.718827e-02, 1.803394e-18, 4.377806e-04, 1.593155e-04, -2.886859e+19, 2.446955e-06, 4.714172e-07, -1.444181e+14, 5.921228e-22, -3.968436e+05, 2.081487e+08, 4.200042e+18, -1.334353e-20, 1.637913e+12, -7.203262e+03, 3.510359e+09, 5.945107e-08, 2.798793e-07, 1.819020e+17, -1.331690e+02, -2.714485e+18, -2.344350e-18, -1.313232e-20, -6.739364e-22, 1.025007e-02, 1.186976e+07, -1.412268e+09, -6.194861e-18, -4.523625e-03, -4.504270e-06, 2.158726e-21, -8.330465e-17, 4.566938e+11, 6.677905e-05, -2.312717e-13, 5.325983e+16, -1.075392e-04, 1.140532e-13, 2.606136e-11, -2.815243e+16, -3.550714e-16, -1.033372e+05, -1.183041e+03, -7.872171e-21, -4.362058e-07, -3.181126e-07, -2.676671e+18, -2.674920e-15, -3.991169e-16, -4.401799e+07, -2.826847e-10, -2.033266e-20, -5.669789e-11, 3.711339e+05, -1.194584e-17, -3.310173e+10, -1.743331e-15, -2.288755e+15, 8.610375e+06, 4.796813e+07, -1.465344e+07, -4.074823e-12, 2.089962e-21, -4.171761e-18, -4.682371e+18, 4.030447e+08, 4.679856e-07, -2.662732e+15, 2.551805e-21, 2.482089e+05, -2.310281e-10, 3.533837e-08, 1.829437e-07, 3.074466e-06, -2.889997e-12, -4.203806e+01, 1.598374e-21, -1.300526e-05, 2.921093e+14, -8.847920e+14, 3.788583e-04, -4.538453e+19, -2.734893e+07, 1.351281e-04, 1.128593e-01, 3.868545e+13, -1.200438e+18, -2.641822e+10, -4.493835e-16, -6.291094e-13, 2.534337e-08, -4.063653e-03, 3.200675e-02, 2.243642e+08, 5.170843e-08, 8.984841e-14, 2.228243e-01, -6.770559e-09, 3.513375e-16, -2.512038e-14, 3.421696e+04, -4.514522e+01, -1.062799e-20, 2.853168e-19, 8.503515e-21, -1.664790e-03, -2.515606e-18, 1.237958e-21, -8.059224e-20, 4.386086e+00, 5.301466e+17, 4.388106e-12, -3.432129e+00, 2.189230e+18, -1.806446e-02, 3.266789e-18, 3.355664e-13, -1.206966e-21, -4.813560e-02, -1.352049e+18, 1.257234e-07, 2.511470e-09, -2.512775e-01, 3.613773e-10, -9.065202e+16, -1.777852e+18, 1.444606e-01, -2.857379e+00, -1.912993e+00, 3.436817e-09, -1.749039e+14, 2.215154e-18, 3.384923e+18, -4.513038e-09, 4.814904e+05, 3.730911e+15, 1.861706e+12, 3.378290e-03, 2.851468e-06, -1.577518e-04, -4.122504e-12, -2.743002e+03, 8.512568e-02, -1.333039e-09, -4.899609e-17, -1.782085e-11, 2.552482e-02, 4.200193e+10, -4.298147e+03, -1.923210e-10, -1.208889e+01, 4.606772e-21, -3.331241e+10, -3.704566e-16, -3.733178e-20, -4.950049e+16, 3.184384e+15, -4.107375e-06, 1.801875e+09, 9.632951e-16, 7.172728e-10, 2.324621e+07, 2.892586e+15, -1.582511e-17, -4.119044e-13, -1.248361e+09, 1.531907e+08, -1.795628e-19, -1.735919e-17, -4.646689e-07, -2.779304e-11, 8.048984e-10, 3.536087e-02, -6.494880e+18, 2.714073e+06, 3.374557e+18, 3.621468e-06, 2.742652e-07, 2.551176e+03, -4.420578e+18, -4.370624e-08, -4.507765e-11, 4.193746e-20, 1.206645e+13, -3.750231e+03, 4.390893e+08, -9.756466e+11, 3.392778e-06, -3.453465e+01, -1.406102e+11, -3.673526e-15, 1.417082e-03, 1.499926e+16, -4.471032e-17, -2.657920e+16, 4.792261e+09, -3.212735e+17, -3.372737e-05, -4.730048e+01, 3.365478e+07, 2.835695e+13, -3.242022e-07, 3.640288e+11, 1.862055e-08, -4.121250e-19, -3.891100e-02, -4.367058e-15, 1.364067e-17, -4.575429e-12, 3.621347e-07, 1.506864e+11, 3.715065e+18, -1.773352e+08, -3.502359e+07, -2.326890e-04, 2.948814e-17, -2.438988e+14, -2.994787e+04, -3.755515e+12, 2.708013e-13, 3.281046e-01, -3.710727e+12, -8.380304e+14, 1.062737e-05, 2.385939e+16, -4.383210e-20, -3.779417e+03, 3.080324e-03, 3.810188e+16, 3.058415e+00, -2.484879e-21, -1.951684e+01, 6.979033e-10, -3.866994e+06, 4.278936e-19, 9.365131e+10, -3.685205e+01, -2.678752e-16, 2.011434e-19, 1.884072e+08, -1.300910e+04, 2.414058e-09, -4.675979e+11, 3.583361e-19, -4.499438e+18, 1.641999e-21, -2.686795e-10, 6.136688e-20, -3.793690e+16, 4.944562e-20, -3.490443e-03, 3.080547e+02, 2.041413e-06, 2.021979e+03, 2.314233e-06, 1.564131e-01, -8.712542e+17, 7.569081e+16, -1.056907e+17, 2.095024e-14, -2.487621e+17, -3.490381e+19, -6.944641e-01, -2.892354e-08, -3.597351e+12, -1.985424e+06, -2.348859e+09, -1.657051e+01, -3.358823e+14, 3.219974e-16, -4.819092e-13, -2.905178e-11, 8.257664e+04, -4.092466e-15, -3.464711e-13, -3.956400e-14, -2.548275e-08, -8.917872e-21, 7.387291e+13, 2.300996e+16, -4.870764e+18, -9.909380e-03, 1.260429e-08, -3.409396e-12, 1.003848e+02, -4.883178e-02, -3.125474e-14, 1.005294e+11, -4.736012e+09, -1.647544e-09, -3.491431e-03, 4.619061e+07, -4.547601e-09, -3.788900e-02, -2.648380e-17, 4.601877e-16, 1.754357e+13, 4.325616e+12, 1.860822e+03, 4.080727e+15, -4.573470e-14, -1.293538e+16, 2.811449e+05, 4.032351e+06, 4.274005e+04, 3.454035e-21, 4.933014e+09, -3.712562e+08, 3.158678e+06, -1.636782e+11, -2.884298e-18, -3.685740e-17, 1.027472e-07, -3.765173e-12, 2.740894e-17, 2.634880e+02, -4.334010e+00, -3.708285e-14, -3.858731e+16, -3.956687e+13, -4.064064e-12, 2.558646e-05, 4.459143e+03, -9.661948e+03, -1.994335e+16, 1.202714e-17, -3.782707e-17, 9.099692e-04, -1.864561e+09, 3.493877e-08, 4.288188e-01, 1.767126e-14, -6.779451e-22, -1.977471e-09, -3.536454e+06, -7.319495e-04, 2.004028e-16, -3.181521e-17, 3.336202e+14, -2.752423e+07, 3.390953e+01, 4.199625e-15, 2.883232e-12, 3.122912e-06, 7.324619e-19, 3.092709e-02, -2.758364e-15, -2.489492e+12, -1.622009e-08, 2.371204e+06, -1.582081e+08, -6.382371e-17],numpy.float64)
        ca(self._r.d2, [1.374233e+19, 2.424327e-04, -1.615609e-02, 3.342963e-21, -4.308134e+14, -1.783430e-07, 2.214302e+18, -1.091018e+17, 3.279396e-20, 2.454183e-01, 1.459922e+07, -3.494941e+16, -7.949200e-21, 1.720101e+17, -1.041015e+16, 1.453541e+05, 1.125846e+06, 1.894394e+07, 1.153038e-17, -3.283589e+06, 2.253268e-10, -3.897051e+06, 1.362011e+05, 5.501697e-19, -4.854610e+01, -1.582705e-05, 7.622313e+04, 2.104642e+08, -1.294512e-06, -1.426230e-19, -4.319619e-15, 9.837716e+03, -4.949316e-01, -2.173576e+02, 2.730509e-19, -2.123803e+05, 1.652596e-17, -2.066863e-09, 3.856560e-08, 1.379652e+18, -2.119906e+16, 4.860679e-05, -1.681801e-10, -1.569650e-15, 3.984306e-21, 3.283336e+08, -9.222510e-16, -3.579521e-02, 1.279363e-05, 3.920153e-12, 4.737275e-15, -4.427587e+06, -3.826670e-14, 2.492484e-04, 4.996082e+09, 4.643228e-11, 2.809952e-17, -2.224883e-13, -4.442602e+18, 4.422736e+11, 4.969282e-18, 4.937908e-15, 6.973867e-22, 1.908796e-19, 4.812115e-08, 1.753516e-02, -3.684764e+02, 1.557482e-17, -1.176997e-11, 1.772798e-05, 4.877622e-16, 1.107926e+11, 4.097985e-14, 2.714049e-18, 3.198732e+15, -1.052497e-01, -5.003982e+07, -1.538353e-04, 3.045308e+17, 1.176208e-18, 1.268710e-10, -1.269719e-05, -2.989599e+00, -3.721343e-11, -1.444196e-10, -2.030635e+04, 2.070258e+16, -3.001278e-14, 1.116018e+14, 4.999239e+15, 4.286177e-21, -2.972550e+10, 3.549075e-20, -2.874186e-06, 2.994430e+09, 2.978356e+10, -2.364977e+07, 2.807278e-01, -3.279567e-10, 4.567428e+05, 1.612242e+07, 4.102315e+05, -1.069501e-20, 2.887812e+10, 4.384194e-09, -2.936771e-11, -4.164448e+07, 3.391389e+04, -3.923673e+17, -2.735518e-22, -2.019257e-01, 3.014806e+15, -3.885050e-15, -2.806241e-20, 3.077066e+18, -1.574438e+14, -3.131588e+19, 4.812541e+03, 4.435881e+16, -3.843380e+02, -7.522165e+03, -3.668055e-21, 2.603478e-08, 2.928775e+08, 2.892123e+00, -1.594119e+04, -4.817379e-01, -2.121948e+03, -8.872132e-09, -3.909318e-06, -3.849648e-14, -4.554589e+18, 4.410297e-15, -2.976295e-04, -2.298802e+10, 4.981337e-07, 5.364781e-12, 1.536953e+07, -4.082889e-07, 1.670759e-21, 4.009147e-13, -4.691543e-18, -2.597887e-13, 2.368696e+18, -2.585884e-07, -5.209726e-03, -2.568300e+06, 2.184692e-20, -1.799204e+16, 1.397292e+04, 4.277966e+13, -4.072388e+09, -2.324749e+16, -4.717399e+10, -2.853124e-05, -3.664750e+11, -3.864796e-08, 3.265198e+07, -3.309827e+19, 3.222296e+03, 2.366113e-19, -3.425143e+14, 1.627821e-08, 4.987622e+00, -1.402489e-17, -1.303904e+15, -2.042850e+17, -1.399340e+09, -3.560871e+05, -4.251240e-21, -7.806581e-10, 1.723498e+00, -2.030115e+08, 4.595621e-19, 1.174387e-10, 3.474174e+14, -4.159866e+03, -1.833464e-19, -3.650925e+05, 3.757361e-03, -1.854280e-10, -1.856982e-13, 1.685338e+08, 4.051670e-11, 4.095232e+03, -2.956025e-16, 4.986423e-05, 4.941458e+10, 4.145946e+11, 3.402975e+14, -1.954363e+11, -2.274907e+10, -3.162121e-17, -5.027950e-07, 4.135173e-02, -3.777913e-04, -4.898637e+15, 2.354747e-02, -6.884549e+13, -1.896920e-05, -1.914414e+15, -1.196744e-19, -4.692974e-01, 8.586675e-10, -2.204766e-17, -3.586447e-14, 1.751276e+17, -2.546189e-05, -2.248796e+03, -9.445830e+02, 1.150138e+03, 4.586691e+11, -2.582686e-15, -2.795788e+12, -3.409768e+07, -2.172186e-03, -1.457882e+06, -4.153022e+13, -4.255977e-08, 3.216237e-07, 4.935803e+02, -4.248965e-16, 1.740357e+07, 4.635370e+19, -4.099930e-14, 2.758885e-16, -4.714106e-05, -4.556226e-20, -4.290894e-19, 1.174284e-09, -1.443257e+16, -2.279471e-08, -3.030819e-16, 1.535128e+18, -3.248271e-07, 3.079855e-21, -3.056403e-02, -1.368113e-12, 4.004190e-10, 4.955150e+07, -2.494283e-16, 2.186037e+05, -1.232946e+03, 5.586112e-05, -2.288144e+17, 2.515602e-19, -4.064132e+08, -3.217400e-02, -2.620215e+07, 2.283421e-14, -1.130075e+08, 3.304955e-03, 1.352402e+01, 6.255755e-03, -3.913649e-08, 5.474984e+01, -4.712294e-08, 3.548418e-16, 1.276896e+12, 2.007320e-08, 3.025617e+04, -2.544836e+14, -2.087825e+17, -3.285556e-09, 2.605304e+07, -1.876210e+07, 3.734943e-10, -3.862726e-15, -4.227362e-05, 1.267773e+14, -1.706991e-05, 3.737441e+10, 2.641527e+01, 4.439891e+10, -1.444933e-05, -2.190034e-12, 8.059924e-18, -1.324313e+18, -1.420214e-10, 3.940158e-20, 3.943349e-02, -2.685925e+19, 4.334133e-05, 3.171371e-21, 2.094486e+12, 1.331741e+03, 1.205892e-02, 1.791416e+04, 3.899239e+10, 6.581991e+06, -3.860368e+11, -3.853916e-02, 1.314566e+09, 3.923126e+03, -3.509905e+13, -4.332430e+06, -1.713419e+01, -1.244104e-14, -5.529613e+01, 6.630349e+06, 1.053668e+10, 3.312332e-05, -1.252220e+08, 3.997107e-07, 1.847068e-13, -2.393157e-11, -2.083719e-10, -4.927155e+11, 2.666499e-15, 4.087292e-10, 4.082567e-10, -2.017655e+07, 9.108015e+15, -4.199693e-15, -4.969705e-17, 1.769881e-02, 1.745504e+00, 2.200377e-16, -4.404838e-06, -1.317122e-15, 7.210560e+08, 1.282439e-18, -3.204957e-06, -1.624277e+05, 4.570975e-22, 1.261776e+04, 4.416193e+12, -4.343457e-18, 4.095420e-14, 4.951026e-09, 2.261753e-15, 4.125062e+05, -4.448849e+11, -3.184924e+06, -2.050956e+05, -9.895539e+09, 4.541548e+11, -4.230580e+11, -4.268059e-15, -4.393836e+09, -2.514832e-08, 3.322394e-04, 2.597384e-18, 1.316619e-11, -2.250081e+16, 2.179579e-10, -1.838295e+04, -1.995626e-17, -4.656110e+17, 3.481814e-07, -2.859273e-11, -2.011768e-06, -1.809342e-17, -3.242126e+10, -1.873723e+08, -2.833009e-12, -3.758282e+12, 2.970198e+15, -2.667738e-01, -3.689173e+11, 1.008362e-10, -1.526867e-20, -1.439753e+06, -6.154602e+16, 4.165816e+00, -1.597823e-09, -1.862803e+14, -2.222766e+15, -2.892587e+17, -4.230426e-14, 2.999121e-21, 1.642245e+00, 1.590694e-14, -4.469755e-06, 2.700655e+12, -1.822443e-02, -4.889338e-16, -3.174990e-11, 4.146024e-03, 1.313280e+01, 3.235142e+15, 3.500547e+00, -4.413708e+03, 1.485548e+16, -1.660821e-11, -4.334510e-22, -1.209739e+04, 1.149570e+12, -4.537849e+00, -3.628402e-16, 2.748853e-12, -4.818907e-21])
        self._r.d3 = numpy.array([9.025110e-18, 3.567231e+17, 2.594489e+01, 2.311708e-04, 7.345164e+13, 6.550284e-01, 1.969554e+12, 9.451979e-05, 5.900637e-09, 9.975667e+03, 6.549533e-17, 2.227145e-13, 2.822132e+18, 4.332600e+18, 1.485466e+05, 5.844952e-14],numpy.float64)
        ca(self._r.d3, [2.047398e-20, 2.091541e-20, 9.084241e+14, 1.583413e+01, 5.168067e-02, 1.360920e-11, 9.818531e-21, 6.293083e+07, 4.406956e-14, 8.540213e-09, 7.329310e-03, 5.566796e+00, 3.968358e-08, 4.928656e-08, 5.994301e-20, 8.281551e-21])
        self._r.d4 = numpy.array([-4.207179e-09, -3.611333e+11, -4.155626e-06, -2.458459e+10, 2.826045e-11, 3.511191e-08, 4.759250e-07, 2.455883e+09, 4.182578e+11, 4.732337e-14, -2.967313e+02, -4.139188e+14, 6.287269e+03],numpy.float64)
        ca(self._r.d4, [2.864760e-08, 3.900663e+13, 9.105789e+11, 2.943743e-15, -2.823159e-16, -3.481261e+19])
        d5_1dat = numpy.array( [-5.528040e-08, 3.832644e-01, -9.139211e-22, -4.919312e-05, 3.809620e-11, 1.751983e-09, 2.207872e-21, 1.432794e+09, -1.970313e+11, 3.405643e-18, -3.756282e+14, -4.918649e+08, -3.162526e-14, -2.853298e-09, 2.835704e+10, 4.458564e+16, 6.657007e+09, 3.640798e-10, 4.950898e-06, 3.384446e+14, -4.065667e+16, -2.243648e-05, 4.822028e-21, 4.231462e-14, -2.526315e+11, -5.626782e-05, 2.321837e+13, 1.772942e-09, 1.606989e-08, 2.669910e-04, -3.635773e+08, -3.967874e-10, 6.599470e+15, 4.612631e-08, -1.417977e-11, -8.066614e-18, 5.738945e+15, 6.408315e+13, 1.922621e+12, 3.096211e-14, -2.079924e+18, 1.664290e+09, -4.502488e+07, 3.092768e+05, 4.414553e+10, -3.673268e+02, -4.772391e+17, -1.100877e+02, -1.453900e+01, 4.293918e-13, -4.270900e-02, -3.886217e+11, -2.206806e+02, 7.034173e-07, -2.826108e-21, 3.616703e-21, -3.385765e+04, -7.027764e-11, 9.684099e+05, -4.248931e+03, -3.415720e-20, -3.315237e-11, -9.555895e+11, 3.520893e-13, 1.089514e-13, 3.591828e-21, -4.847746e-06, -2.678605e-16, -7.480139e-04, 2.208833e+01, 1.075027e-07, -1.047160e-05, 2.309356e+06, 7.308158e-19, -4.915658e+02, 4.634137e+18, -3.682525e+13, 4.124301e-06, 4.158100e-10, 2.091672e-11, -6.856023e+07, 8.418116e-07, -1.655783e-13, -2.502703e-03, 1.274299e+17, -4.784498e-20, 1.357464e-10, 4.107075e-13, -2.753087e-05, -2.594853e-14, -3.712038e-13, 1.143743e+14, -2.495491e+10, 2.331111e-15, 2.987117e+18, 2.876066e-18]) +1j* numpy.array([-8.370342e-05, -2.348729e+14, 3.257323e-03, 4.131177e+03, 2.161235e-13, -4.721350e-09, 1.995494e+02, -3.671161e+01, 3.577448e-08, -2.106472e+17, 4.470172e-10, 4.042179e-18, -6.516616e+06, -3.452557e+08, -2.995060e-12, 7.108923e+00, -3.211521e+12, -3.543511e+12, -4.990060e+10, -1.078185e+12, -4.563018e+11, -4.127342e-07, 3.047283e-13, -7.096004e-20, -3.751135e+15, -1.121229e+06, 2.090954e-11, -2.086763e-11, 4.890986e+07, -2.309172e+13, 1.621930e-07, -4.366606e+11, 3.614235e+10, -1.482655e+07, -2.064002e+14, 4.607724e-09, 1.349841e+16, 2.340153e-02, -4.978818e-20, -4.310755e-08, -3.092006e+17, 2.129876e-14, 3.521718e-09, 1.785216e-09, 3.359563e+13, 4.071776e-16, 1.436872e-20, -3.517250e+05, 5.252845e-07, 7.469291e-01, -4.355370e+18, -1.421206e+15, 1.153528e+15, 7.734075e+01, -4.073023e-10, -4.657975e-13, -4.290567e-03, -4.795922e-13, -5.476246e+01, -4.044947e+00, 2.545910e-04, 3.937911e+13, -9.652266e-02, -5.878603e-07, 1.205180e-04, 4.153653e+16, 4.943621e-18, 4.347876e+13, 4.479099e+04, -3.199240e-04, 2.432062e+06, 2.478472e-20, 4.684549e-17, 3.321873e-04, -3.465954e+04, 4.173493e+02, -2.258389e+19, 3.365401e+10, -2.122599e+09, -2.071802e+06, 2.590336e+09, 3.335575e+06, -4.325264e-03, 4.529918e+14, -4.182319e-18, -3.928899e+02, -2.170676e+06, -1.918490e-17, 1.227619e-21, 2.607308e+04, -2.312853e-15, 4.028300e-17, -3.146932e-11, 9.543032e-05, -4.535571e+12, -3.423998e-17])
        d5_1=numpy.array(d5_1dat).reshape([8, 6, 2],order="F")
        self._r.d5 = d5_1
        d5_2 = self._r.d5
        ca(d5_2.shape, [5, 6, 5])
        ca(d5_2.real.flatten(order="F"), [4.427272e-10, -1.149547e-08, -1.134096e+16, -4.932974e-03, -7.702447e-01, -3.468374e-03, -5.037849e-14, -4.140513e-08, 4.553774e+03, 2.746211e+01, -4.388241e-17, 2.262009e+00, 5.239907e+06, 4.665437e-05, -1.662221e-05, 5.471877e-13, 2.592797e+11, -4.109763e-05, 1.797563e-04, 1.654153e+01, 4.011197e+07, -2.261820e-10, 5.836798e+02, 1.518876e-18, 4.814150e+18, -4.610985e-07, -3.126663e-07, -1.981883e+10, 4.117556e-02, 1.937380e-07, 1.397017e-10, 2.809413e-17, 9.387278e+18, 4.777753e-11, -4.248411e+15, 3.851890e-16, -1.598907e-08, 3.699930e+14, 2.763725e-08, -4.130363e+17, 3.105159e+06, -2.026574e+00, 3.956735e+01, 3.893311e-04, 3.574216e+13, 3.618918e+03, -4.027656e-09, 9.174470e-02, -8.108362e-21, 1.857260e-18, -3.540422e+13, -2.985196e+12, -3.219711e-08, -1.618670e-13, -2.648920e+12, 1.224910e-14, -4.740355e-03, 4.604337e-18, 3.809723e+05, -4.460252e+15, 1.894675e-15, -4.141572e-08, -3.939165e-09, -1.916940e-06, -2.382435e+16, -4.689458e-01, 1.498825e+17, 1.876067e-15, -1.801776e+09, -1.140569e-05, -6.881731e-08, -4.835017e-07, 3.843821e-17, 2.220728e+06, -4.321528e+10, -3.950910e+01, -1.732064e-11, 3.009556e-16, -3.509908e+18, -7.781366e-15, -2.511896e-18, -2.037492e+04, 2.656214e-19, 2.163108e+16, 4.526743e+19, 2.738915e-11, 8.491186e-16, -1.286244e+05, 3.635668e+12, -4.964943e+15, 3.725194e+05, -4.010695e-19, 2.140069e-09, 3.957374e+19, 4.478530e-06, 4.284617e-06, -3.459065e+12, 1.525227e-18, 4.892990e+06, 3.557063e+07, 2.986931e+18, 2.147683e-05, -4.190776e+17, -3.715918e-14, -3.448233e+01, 1.272542e+15, -3.900619e-06, -3.712080e+05, 3.388577e+04, -4.440968e-11, -4.395263e+18, -4.052174e-06, -3.065725e+00, 3.915471e-04, 4.863505e+12, 4.861871e-09, 4.607456e+03, -1.845908e-12, -9.985457e-11, -4.534696e-08, -1.163049e-17, 4.492446e-11, 3.078345e+06, 8.520733e+05, 2.218171e+14, -4.546400e+09, 4.641295e+09, -1.677260e-07, 9.650426e+04, -4.001218e-04, 4.761655e-22, -3.989865e+01, -5.800472e-08, -2.548565e-01, 4.648520e-08, 4.255433e-16, -2.387043e-11, 4.172928e+17, 4.194274e-12, -1.391555e-04, -1.063723e-01, 1.609824e-13, 9.196780e-10, -4.744075e+06, -4.764303e-02, -4.540535e-10, -4.361282e+00, -1.460081e+01, -2.215205e-16, 4.652514e-19])
        ca(d5_2.imag.flatten(order="F"), [-3.227745e-11, 3.306640e+04, 5.733779e-03, -4.965007e+12, -1.568029e-15, -3.008122e+08, -2.135053e-06, -2.406927e+10, 3.292783e+05, 4.388607e+01, -1.765870e+18, -1.356810e+11, -1.227140e-17, -4.613695e-13, -2.700191e-03, -3.556736e-15, -2.019073e-03, -4.766186e+11, 6.689841e-18, 3.052622e+03, 1.277135e-05, -3.121487e+15, -3.821687e+10, 1.168559e+17, 3.894338e+02, 1.815897e-01, -2.028013e-16, -1.291271e-04, -4.564800e+01, -1.537011e-11, 2.585832e-08, -1.369181e-21, -1.508252e+19, 7.819509e+14, -8.344493e+11, -3.658894e-04, 3.591114e+08, -3.293697e+00, 3.409179e+08, -3.879994e+18, 3.766739e-07, 2.334020e+17, -3.558653e-14, 4.718551e-03, -4.986314e+05, 7.019211e-03, -4.789392e-02, 1.732946e-11, 2.863924e+06, 4.353270e-09, -2.371537e+06, 3.279747e+07, -4.805626e-20, 2.621159e-16, 3.031856e-04, 1.224164e-13, -5.887172e+11, -2.589087e-05, -2.936782e+18, -1.259862e+08, -2.475554e-02, -3.565598e+04, 1.708734e+00, -1.844813e+00, 3.616480e+10, 3.944236e-01, 3.669220e+06, -3.385628e-15, -2.178730e+01, 4.619591e-17, 2.250613e-10, 7.894372e+11, -3.258819e-19, -3.287104e+01, 4.524240e-14, 3.506383e-08, -1.023590e+02, -1.400509e-20, 3.294976e-07, -3.740683e+07, -1.408191e+04, -4.009454e-12, 3.780340e-11, -1.697898e-04, 3.329524e-02, -2.017186e-08, -4.107569e-09, 3.223035e-18, -2.305074e+12, -4.410777e+09, -1.776812e+05, -2.204486e+03, 3.928842e+00, 8.164433e-19, -3.205076e-12, 4.395648e-17, -4.112187e-04, 3.032568e+19, -1.555449e-04, -1.139386e+19, 1.296998e+15, 2.120574e+06, -3.686849e+05, -2.367773e+08, -1.322619e+10, -4.118283e-11, 4.910520e+08, 2.833307e+14, 1.921342e+02, 3.152412e+19, 1.676044e+05, -3.724410e-18, 2.819222e+04, 2.091958e+00, -4.193395e+05, -4.363602e-11, 4.613626e+02, 1.208108e+18, 1.149369e-01, 1.258756e-07, 3.502706e-04, 1.020676e-19, 2.822635e-03, -1.578762e-14, -4.171860e-19, -2.410204e-16, -2.000543e+13, 3.060033e+16, 4.215806e+09, -3.419002e+13, -2.856480e-11, -2.210954e-12, 3.305456e+03, -3.624269e-13, 3.099517e-05, -1.411512e-10, -1.566814e-06, -9.637734e-19, 8.972782e+09, 4.064705e+08, 4.784309e+14, -8.230735e-01, 2.129415e+19, -3.169789e+05, 8.918012e-19, 2.172419e-18, 4.803547e-17, 1.503276e-10, 4.251650e-21, -4.256823e-12])

        self._r.s1 = 3847.9283
        val=self._r.s1
        #if self._r.s1 != 7.8573:
            #raise Exception()
        self._r.s2 = numpy.array([-1.374271e+12, 1.798486e-08, -4.845395e-08, -4.785331e+12, -2.914127e+04, -1.753064e-17, -4.063563e-09, 2.758058e+04, -1.988908e+11, -1.535073e-18, 2.439972e-02, -3.237377e-12, 9.760366e-12, -4.276470e-21, 1.693848e+18, -1.401259e-19, -3.140953e-11, 8.675222e-05, -2.097894e+05, -1.183071e+09, -4.405535e-14, -1.157335e+11, 1.055748e-19, 2.363738e+19, -1.404713e+19, 4.284715e+01, -3.515661e+19, -1.254196e+13, 2.076816e+19, -2.454920e+04, -2.205493e-21, -9.940678e+08, 3.818785e+03, -1.504647e-14, -2.604226e+15, -3.708269e+10, -1.633861e-19, -2.928434e+06, -3.741304e-01, 3.925411e+09, 1.135659e+05, 8.774251e-11, 8.857955e-17, 1.461853e-18, 2.228531e+18, -2.901828e-21, 2.648299e+17, -1.981382e-08, -8.234543e-19, -1.732653e+07, 1.899980e+10, -1.392906e-08, -6.839790e+14, -2.267130e+09, -4.215074e-14, 4.329019e-17, -3.351069e+09, -2.689165e-07, -4.337995e+10, 4.010095e-15, 1.340637e-05, -4.157322e-06, -1.091954e+14, 1.108454e-11, -8.934548e+08, -3.823683e+14, -3.164062e+07, 2.908637e-08, 8.450160e+02, 4.285117e+16, -2.603674e+05, -5.280737e-07, -2.589230e-05, -9.163516e+17, -3.501593e+04, -4.513991e+06, 3.740032e+11, 6.325982e+08, 4.911299e+19, -3.871696e-08, -1.641252e+00, -3.909808e-17, 4.148389e-21, 3.153334e-06, -2.737137e-07, -2.885790e-08, -2.024930e+09, 7.689509e+05, -7.910094e+00, -3.122012e-08, 2.087070e-07, 2.943975e-08, -3.637942e-05, 1.265381e-18, -3.240420e-07, -3.299393e+15, -4.534857e+15, -4.197434e+05, 2.443365e-06, -1.220755e-17, 2.294507e+06, 1.755297e-21, 9.738120e-03, 3.730024e+12, 4.634193e+11, -4.594819e-08, -1.281819e-03, 1.860462e-04, -3.678588e+18, 4.460823e-18, -1.766008e+14, -2.775941e+11, 4.325192e-07, 2.655889e+10, -1.757890e-06, -2.103859e-08, -2.269309e+12, -9.581594e-11, -2.672596e+14, -3.052604e+04, -2.464821e+18, -4.276556e+02, -4.032948e+05, -2.305644e+19, 4.750717e-04, 6.464633e+03, 7.776986e+17, -2.123569e+16, 3.016544e-07, -2.520361e-03, 2.920953e+00, 3.216560e-12, -1.880309e+10, 9.663709e+16, 1.981875e-02, 1.826399e+19, -1.218763e-21, 1.673439e-10, -1.995639e-05, -2.134349e-02, -3.101600e+11, -1.148683e-14, 1.527847e-11, -4.532247e+08, 4.120685e-21, 4.836973e+16, 4.509629e-05, 3.936905e+17, -7.068550e+07, 4.976433e+02, 2.118027e+02, 4.972063e+06, 4.601005e+16, -4.367053e-17, 1.770987e+06, 2.572953e+00, 3.020633e+12, 1.762052e+11, 4.443317e-05, -1.896787e+08, 3.349722e-14, 1.094784e+06, 2.239828e+00, -1.400895e+05, -1.098610e+09, -3.681296e-09, 2.842120e+16, 3.138041e-18, 1.993332e+07, -2.584283e-06, -4.399412e+12, -7.050502e-19, 1.079255e-10, 2.938524e-19, 4.733761e+07, 4.451092e+02, 1.326299e-17, 2.808418e+12, -2.952152e-14, 4.550734e-16, -2.399796e-04, -2.786184e+07, -3.567595e+03, -2.166879e+19, -1.804263e+04, -9.775023e+09, 4.758856e+09, 2.636609e+13, 4.132205e+10, 2.594126e-20, -3.244046e-18, -3.136448e-03, -3.446778e+08, 2.442233e-12, 1.808183e-11, -2.846331e+02, -2.933024e-10, 3.547133e+00, -9.445332e-20, -4.328694e-04, 2.748924e-12, 4.169152e+10, -3.488881e-04, -2.713158e-08, -1.549705e+15, -3.554349e-08, 2.503210e+14, 1.715581e+08, -2.047344e-10, -4.017695e+05, -1.979563e-08, 4.032794e+07, -1.670813e+07, 1.889040e+07, 4.875386e+11, -1.159781e+13, -4.023926e-21, 4.535123e-07, 4.470134e+02, -2.619788e+04, -3.454762e-09, 3.006657e+00, 1.158020e-13, 1.885629e-11, -3.766239e+15, -6.418825e-20, 3.322471e+13, 4.646194e-07, -2.817521e+13, 1.370796e-04, 4.014727e+04, 3.057565e+18, -6.171067e-12, -4.067906e-16],numpy.float32)
        #ca(self._r.s2, [3.252887e+09, 1.028386e-04, -2.059613e+01, 1.007636e-14, -4.700457e-13, -1.090360e-22, -3.631036e-15, 2.755136e-09, 4.973340e+13, 2.387752e-15, -9.100005e+06, 1.484377e+13, -2.287445e-13, -3.718729e+18, -4.771899e+19, 8.743697e+13, 1.581741e+07, 2.095840e-09, -5.591798e-03, 6.596514e-06, -1.006281e+05, -4.126461e+12, 4.246598e-20, -1.376394e+08, -3.398176e-03, -1.360713e-21, 3.109012e+14, -8.112052e+07, -8.118389e-02, -3.455658e+14, 7.352656e+12, 4.198051e+06, 4.258925e-03, -2.634416e+12, 3.362617e+02, -4.606198e-15, 4.228381e-19, 4.209756e-15, -1.268658e+05, 3.019326e+02, 7.937019e-01, 6.225705e-09, 1.324805e-19, -4.355122e+01, -4.533376e+15, -1.584597e+01, 1.657669e-02, -3.720590e-18, 2.038227e-04, 2.890815e+04, 1.513743e-14, 4.993242e-20, -5.255463e-21, -8.084456e-14, 4.087952e-09, 2.518775e-21, 4.977447e+15, 3.363414e-19, -3.931790e-20, -7.810002e+14, -3.589876e+14, -4.969319e-18, -4.356951e-20, -3.682676e+02, -1.319524e+10, 3.805770e-11, 2.134369e-10, 3.684259e-08, -2.901651e-13, -4.486479e-01, 2.208715e-02, 3.224455e-01, -3.305078e+09, -3.326595e-02, -2.473907e+03, 3.608010e-15, -2.596035e-01, 2.594405e-01, -7.569236e-01, -3.430125e+09, 2.920327e+02, -3.763994e-12, 2.617484e-12, 4.808183e-07, 3.885462e+15, -1.201067e+00, 1.887956e+06, -4.038215e+02, -4.710561e+03, 1.659911e-16, -4.955908e-17, 4.681019e-09, 3.945566e+05, -3.433671e+19, -2.679188e+05, -2.357385e-01, 2.891702e-19, -4.464828e-06, -6.003872e-04, 1.369236e+18, -3.597765e+01, -4.246195e+08, -4.765202e+17, 4.472442e+10, -1.038235e-05, -4.632604e-09, -2.484805e-15, -7.998089e-16, -3.690202e-04, -3.276282e-04, 1.966751e+10, -5.081691e-18, -2.004207e-05, -2.756564e-03, -2.624997e+14, 2.398072e-20, -4.098639e-10, 2.930848e+01, 8.983185e+15, 1.984647e-15, 1.331362e-16, -6.519556e+15, 4.270991e+15, -9.165583e-13, 4.266535e+17, 4.238873e-21, -2.487233e+17, 4.904756e+03, 2.692900e+10, 1.467677e-18, -2.204474e+06, -1.806552e-09, 9.617557e+17, -1.988740e-20, 1.713683e-04, -2.360154e-21, 4.178035e-17, 2.600320e+12, -4.761743e+09, 3.034447e-20, 4.941916e-06, -1.373800e+04, 1.851938e-09, 1.304650e+14, 3.067267e+07, -4.100706e-06, 2.190569e-03, 5.901064e-17, -2.152004e+15, 4.050525e+04, 3.769441e-06, -4.388331e-12, 1.037797e+12, 3.512642e-19, 3.857774e-09, 1.036342e+03, 3.683616e-18, 9.785759e+10, 2.199992e+03, -2.435347e-02, 1.526312e+06, 2.569847e+14, -2.288773e-01, 4.724374e-06, -3.807381e+13, 2.924748e-10, 2.820652e-20, 4.835786e-12, 2.811112e+02, -6.431253e+02, -4.843622e-06, 1.676490e-10, -4.432839e+07, 1.661883e+19, 8.668906e+07, 2.256498e-04, 2.170563e-01, 1.013347e-17, -4.271306e+11, -2.431836e-17, 3.983056e+02, 4.236306e+05, -2.142877e-20, -2.760277e-12, -8.479624e-08, 2.903436e+05, -3.288277e-17, 4.173384e-10, -1.598824e-08, 8.702005e+05, -1.456065e+08, 2.035918e+06, -1.445426e+02, -4.148981e+05, 4.439242e+02, -1.223582e+16, -8.226224e+14, 1.690797e+16, 1.683472e-04, -4.809448e-16, 4.517499e+06, 4.369645e+02, -4.532906e+09, -3.539758e+07, -2.406254e+01, 4.396602e+00, 2.995832e-01, -2.953563e-04, 3.412885e+17, 1.386922e-17, -2.177566e-04, 2.548426e+04, -3.937000e+16, 2.578962e+02, 2.423257e+16, 3.069379e+09, -4.940417e+09, -4.618109e-13, -1.387521e-11, -2.168721e-05, 1.917758e-01, -3.144071e+03, -1.045706e-13, -2.869528e+02, 2.072101e-13, 4.267714e+12, -2.063457e-19, -3.025547e-12, 8.101894e+10, -4.196343e-04, 4.753178e+18, -2.286673e+08, -2.618986e-10, 3.949400e-10, -4.390776e+12, -2.498438e+10, 3.800599e+12, -3.704880e+15, -4.173265e+02, 3.326208e+19, -1.093729e-21, 3.042615e+16, -1.711401e-09, 3.039417e-19, -2.250917e+15, 2.195224e-01, -2.953402e+05, -1.486595e+17, -2.387631e+00, -1.634038e-14, 6.153862e-18, -3.842447e+05, 3.238062e-14, -4.341436e-11, -1.816909e-19, -3.534227e+14, 8.578481e+07, -4.067319e+09, -4.680605e-08, 4.050820e+04, 1.715798e-11, -5.232958e-12, 2.291111e-07, 1.086749e+01, -3.028170e-14, -6.277956e+13, -1.639431e+11, 4.158870e+17, -1.208390e-18, 4.835438e-05, -3.135780e-08, -4.087485e-12, 2.466489e-08, 1.949774e+00, -3.532671e-21, -1.422500e+12, 4.352509e+03, -1.444274e-17, -1.162523e+19, -4.815817e-07, -2.809045e+11, -1.212605e+03, -3.496461e-08, 6.743426e-18, -4.226437e-06, -3.627025e+07, 1.037303e-05, 2.411375e+08, -2.721538e+12, -4.809954e-06, 4.578909e+16, 9.257324e+06, 4.326725e-03, 4.416348e+12, 4.424289e+13, 3.180453e+12, -6.028285e-10, 3.344767e-14, -2.747083e+18, 1.133844e-15, 3.922737e-06, -3.199165e+00, 2.417553e+02, 3.015159e-20, 2.119116e-02, 4.019055e-09, 3.368508e-21, -1.613240e-19, 3.832120e-14, 1.202460e+17, -3.304317e+19, 1.692435e+17, -2.597919e-05, 3.916656e+17, 4.821767e+06, 4.372030e+02, 1.987821e-08, -1.976171e-08, 1.319708e-09, -4.213393e+10, 3.829773e-15, -4.762296e-21, 4.642216e-18, 1.662453e-13, 6.642151e+03, 2.539859e-02, -3.112435e+09, -3.627296e-20, -1.660860e+02, -3.678133e+07, 3.428538e-01, -2.277414e-20, 2.228723e+17, -2.833075e-06, 9.084647e+03, -2.976724e-16, 2.778621e+15, -2.806941e+07, -1.626680e-15, -4.658307e+13, 7.967425e-11, -2.793553e-21, 4.778914e+16, -6.145348e-21, -4.883096e+11, 1.338180e+04, 7.533078e-16, 3.252210e+05, -2.882071e+10, -2.754393e-06, -1.689511e-16, -1.979567e-10, 4.494219e-04, 3.285918e-15, -4.347530e+05, -1.085549e+15, 1.301914e+07, 3.855885e+13, 3.036668e-11, -4.706690e+12, 3.727706e+17, -4.446726e-12, -4.829207e-08, -1.543068e-10, -2.473439e-11, -2.718383e+13, -4.211115e-21, 3.327305e-04, -1.084328e-20, 3.849147e+06, -1.321415e+09, -3.518365e+07, 2.246762e-21, 2.482377e+11, -4.265765e+03, -4.538240e-05, 2.727905e+18, -2.383417e-13, 4.103955e+04, 8.015918e-06, -2.965433e-18, 3.156148e+03, 8.093784e+18, 4.868456e-12, 1.048517e-02, 1.112546e-19, -3.751041e-12, -3.734735e-06, 3.019242e+06, -1.480620e-17, -3.405209e+07, -1.123121e+19, 8.155940e-20, 1.406270e-17, 2.154811e-13, 9.943784e-20, 1.523222e-17, 6.987695e-21, 8.826612e-12, -2.325400e-20, 3.700035e+15, -5.559864e-11, -8.568613e+10, 1.434826e-07, -2.080666e-03, -2.548367e-03, -4.310036e-18, 3.104310e+00, -3.862149e+17, -4.092146e-13, 3.538555e-14, -4.950494e-05, 6.538592e-13, -4.196452e-11, 2.351540e-01, -1.232819e-01, -3.669909e-21, 1.528733e-14, 5.661038e-15, -1.967561e-07, -2.284653e+02, -1.834055e-10, -2.175838e+05, 4.247123e+06, 1.184396e+18, 4.156451e+15, -4.992962e-14, -2.351371e+06, -6.698828e-10, 2.897660e+17, -3.470945e-06, 4.630531e-07, -4.453066e+10, 4.069905e+09, -4.459990e-08, 4.702875e-13, -2.780085e+17, 1.293190e-05, 2.227539e-03, 1.534749e-21, 7.390197e-02, 4.522731e-10, -1.224482e-02, -3.996613e+02, -1.057415e-15, -7.371987e+14, 4.291850e-02, -4.243906e-08, -3.540067e-04, 4.535024e+09, -3.027997e+10, -3.986030e-02, 1.722268e-04, -3.140633e-20, 3.343419e+08, 4.713552e+14, -3.190084e+05, 2.449921e-01, 2.727707e+14, -3.545034e+11, 2.417031e+13, -2.231984e-09, 3.533907e+16, -4.662490e+16, 3.355255e+14, -1.567147e+17, -3.525342e+12, -3.586213e-16, -4.002334e+15, -1.928710e+08, -4.718466e+04, -1.539948e-06, 3.135775e-11, 3.862573e-10, -3.105881e+08, 4.421002e-05, -2.369372e+01, 4.758588e+13, -1.044237e-15, -4.535182e-10, 1.330691e+18, 3.636776e-01, -4.068160e-12, 2.757635e-17, 3.247733e+13, 1.247297e+06, 5.806444e-13, 3.521773e-05, 4.589556e-14, 1.582423e+00, -1.676589e+00, -3.864168e-07, -3.042233e-02, 2.007608e+14, 4.852709e+02, -2.817610e-04, -1.882581e+19, 1.057355e-14, 4.090583e-04, -1.848867e-13, -5.463239e+13, -1.041751e+05, 3.457778e-01, -2.562492e+00, -6.751192e-10, 1.688925e-21, 3.884825e-07, 1.592184e-12, -2.039492e+06, -1.196369e+19, 2.200758e+00, 2.550363e-21, 7.597233e+06, -1.929970e+09, 1.939371e+03, -3.236665e+09, -1.313563e-13, 2.007932e+02, -3.028637e-02, -1.532002e+00, 2.165843e+17, -3.511274e-04, -3.777840e+15, 1.645100e+17, 3.088818e-07, -2.793421e-11, -4.286222e-01, 4.385008e-10, -2.105222e-01, -2.212440e+08, 2.684288e-01, 1.407909e+18, -3.881776e+08, 3.505820e-09, 3.555082e-19, 3.573406e+01, 4.042915e-19, 2.066432e+08, -2.467607e+10, 3.453929e+01, 4.297309e-14, 1.256314e-11, 8.930289e+14, -3.662200e-03, 2.075690e-16, -2.866809e-17, 4.394016e+10, -2.014195e-03, -3.738633e+12, -4.953528e-05, 3.710240e+06, 3.319208e+04, -5.762511e-20, -4.690619e+16, 3.412186e+19, -1.241859e+09, -4.081991e+12, 4.622142e+03, -1.285855e-02, 1.532736e-08, -2.364101e+09, -1.369113e-18, -2.168979e+19, 2.952627e-14, -2.358172e-16, -1.992288e+00, -9.180203e+12, 1.675986e+07, 4.817708e+06, -1.624530e+06, 4.857415e-01, -5.995664e-03, 1.874911e+08, -3.320425e-17, 5.469104e-02, -3.069767e+11, 8.084999e+12, -2.321768e-20, 1.920249e-06, -4.114087e-02, 3.244903e-04, 3.203402e-17, 4.143519e+06, 4.093124e+17, 4.456464e-15, -2.262509e-13, 4.856535e-08, -4.550552e-15, -3.011803e+18, -2.882488e+13, -2.690616e-04, -3.996010e-19, -4.438855e+18, -1.942208e+03, 1.934537e+18, -1.961547e-07, 4.970021e+17, -3.531211e-17, 4.187133e+04, 2.854106e-12, -2.313257e+13, -3.471439e+16, -6.829753e-16, -4.338617e+03, 5.552258e+05, 1.520718e+19, -2.527013e+14, -2.732660e-09, -1.957740e+11, -4.767907e+12, -4.837256e+18, 3.155432e-12, -3.278156e-04, -1.117720e-13, -3.838176e+11, -7.207202e+08, -4.075808e-21, 1.659402e-14, -4.301886e-19, -4.461337e-11, 2.200979e+15, 4.339143e+07, 5.071459e-06, 1.832776e+18, -2.698948e+03, 4.682397e+01, 2.801081e-08, -3.424292e+00, -5.130555e+14, 1.229975e-14, 2.383361e-09, -3.611087e-07, -2.576595e-07, 1.295398e-08, -2.525216e-11, -2.546657e+10, 9.501518e+03, 8.325605e+04, -1.382092e+02, 2.169085e-21, 4.019485e+16, -2.404251e+17, 1.154833e+10, 9.454498e+01, -7.888753e-09, -4.907318e-20, 1.373262e+08, -2.295105e-21, 1.329034e+17, -3.403883e-20, 3.500734e-03, 2.657397e-20, 4.956090e-07, -2.191353e-03, -1.879262e+09, 4.519858e-14, 4.592234e-14, -1.473612e+11, 4.425251e+10, -3.936903e-01, -2.866089e+09, -3.046203e-09, -4.818832e+01, 2.460150e+02, 2.944622e-11, -1.675111e-20, -1.206111e+01, 5.044200e-13, 3.225861e+02, 3.170008e+12, 1.964043e-20, 3.464033e+03, 1.286135e-08, -6.425529e-10, -4.630162e-02, 2.616476e+18, 4.853669e+03, -1.851316e-03, 1.262159e-02, -1.816675e-12, 3.753560e+14, -3.033601e-18, 1.915137e-02, 3.411614e-14, 4.849348e+05, 3.033922e+13, 3.174852e-17, -4.397997e-09, -9.549484e-01, -1.706859e+11, -3.009122e-01, -8.189854e-15, 4.122789e-17, -1.351025e-13, -2.365671e-10, -1.139709e-05, -2.020593e+10, 3.664729e+14, 1.170917e+00, 1.157248e-19, -4.189734e+17, -4.407278e+13, 4.776929e+18, -3.279961e+07, -4.740186e-15, -3.764392e-02, -2.193781e+18, -4.556987e+00, -3.170243e-18, -1.755775e-16, -2.163959e-03, 2.410150e+11, 1.215874e-18, -4.927956e-05, 2.252375e-06, -3.315242e-14, -3.476357e+16, -4.545391e+00, 6.072704e-13, -4.571860e+09, -2.297081e-02, 2.401997e+10, -6.449709e+05, -3.580234e-08, -5.390535e+08, -4.891390e-19, 3.441769e-09, 4.885513e-09, -4.897531e-10, -1.792753e+08, 2.048965e+13, 3.339876e-21, 4.140957e+04, 2.022520e-21, 5.983159e+06, 1.938164e+13, 2.796107e-19, -1.975692e+09, -2.106710e+15, -4.482226e+09, -2.968068e-19, -1.171747e-03, 1.579378e-01, -4.568752e+16, 2.593340e+11, 3.441530e+10, 3.461992e-01, -5.333082e-09, -4.611969e-12, -4.262468e+19, -4.367063e+01, -2.447378e-11, -3.554859e+02, 4.824680e-05, -1.122071e+11, -2.226371e+13, 3.917182e-17, -1.308204e+10, 4.105055e-16, 5.087060e+07, 7.102691e-05, -2.872202e+03, 1.711266e+11, 3.331993e-08, -1.313944e-08, 3.648109e+11, 5.394321e+01, -4.125398e+03, 3.460645e-02, 2.573745e-18, -1.376298e+01, -3.283028e-05, 3.939711e-12, 3.986184e+17, 2.619889e-11, -4.318052e-09, 1.410821e+00, 3.547585e-07, 4.046432e-17, 1.880087e-07, 1.867841e-05, -1.383592e-21, 2.972106e-05, 2.867092e+01, 3.092781e+03, -6.897683e-02, -1.707761e-04, -4.231430e-11, -3.796784e+00, -2.953699e+11, 3.691013e+09, -3.962307e-12, -1.335633e-17, -1.759192e-01, -4.332862e+04, 1.044899e+11, -2.126883e+03, 1.948593e+14, -2.173759e-05, -4.393250e+05, 1.626217e+08, 2.832086e+18, 4.655433e+03, 2.944186e+08, 2.864233e+03, -3.565216e+05, -4.667000e+11, -3.739551e-03, 3.137195e+05, 2.044129e+19, 2.629232e+14, 3.119859e-09, 3.656121e-15, -4.844114e-03, -2.641449e-11, -3.788231e+05, 2.803203e+17, -3.764787e+09, -6.009761e-08, 4.106308e+01, -2.071363e-20, 1.884576e-20, 2.654081e+11, -3.456281e-11, -4.760486e-02, 4.096057e+11, 4.346738e-11, 2.827941e-02, -1.946717e+08, -9.067051e+15, 4.331454e-14, 4.792779e-09, -4.738308e+18, -1.228815e-09, 2.097152e+16, -4.440036e-06, -3.762990e+02, -2.642879e+12, 3.100004e+10, 3.604336e+12, -3.951650e+11, -1.023763e+15, 4.908325e+17, 2.123963e-19, -1.744445e+09, -2.874189e-06, 2.208907e-08, -2.353407e+10, -1.020581e-03, 1.689180e-01, -2.563565e-12, -1.220758e-15, -2.657970e-16, 1.140528e+10, -2.802143e+14, -3.835574e+00])
        self._r.i8_1 = 45
        if self._r.i8_1 != -66:
            raise Exception()
        self._r.i8_2 = numpy.array([-66, 34, -121, -118, -12, -83, -43, 55, -53, 31, -100, -37, -116, 69, 22, -60, 59, 32, 51, 46, 109, 36, 31, 49, -99, -69, -99, -89, 27, -18, -77, -63, -101, -122, -60, 58, -76, -86, 58, 49, 48, -67, 54, 48, -30, -26, 95, 42, -13, 17, -93, -34, 28, -49, 8, 122, 22, -72, 109, 103, 15, -81, -73, -53, -112, -52, -54, -81, -126, 35, 3, -102, -125, 67, 125, 44, -48, 95, -18, -103, 114, -86, 108, -37, 70, 48, 7, 19, 0, 35, -104, 2, -51, -9, 70, 41, 118, -43, -71, 59, 32, 36, -10, -2, -76, -18, -93, -80, -27, -51, -70, -87, 48, -98, 5, 72, -120, 86, 62, 69, -94, 23, 71, -124, -88, 34, -65, 6, 33, 73, -101, 40, -104, 17, -68, 53, -55, -11, 12, 24, -63, 121, 98, 58, 125, -13, 6, 49, 71, -72, -22, 53, 83, -97, 87, -117, -26, 6, 93, -98, 82, -111, -84, 23, -73, -10, -34, -118, 64, -89, -4, -104, -83, -52, 8, 64, -81, 33, -91, 41, -43, 12, -66, 31, -17, 46, 91, 9, -124, -117, 108, -15, -39, -92, 29, 116, -93, 107, 58, -7, -35, -116, -52, -11, -35, 66, 6, 32, -34, -123, -102, 102, 123, -104, 51, 80, -84, 71, -65, -4, -121, 123, -87, -21, -124, 63, 122, 74, -31, 123, -31, -63, -106, -82, -24, -42, -30, -126, 0, -38, 127, -13, 101, 60, 104, 54, -25, 50, -19, -93, 2, -48, 99, -59, 103, 28, 44, -7, -58, -19, -55, 17, 58, 15, -23, 75, 58, 11, -2, 104, -58, -73, 56, 84, 34, -4, -101, 10, -106, 41, -88, 15, -117, 5, -63, -106, -9, 40, -115, 47, 99, -66, 120, 126, 5, -62, 8, -111, 123, 92, 122, 24, -31, -65, 115, -43, 5, 56, 49, 102, -29, 65, 97, 20, -90, -39, 40, 75, -43, -47, 86, -104, -32, -90, 14, 13, -75, 8, -9, 104, 122, -24, 77, 10, -100, 26, 0, 35, 55, -10, 17, 22, -29, 115, 117, -10, -54, 37, 46, 48, -28, -105, 20, -117, 73, 93, -63, 9, -125, -94, 57, 119, -10, 11, 49, -57, -14, -107, 90, 72, 96, 55, 86, 81, -86, -70, -125, 17, 100, -91, -70, 87, 29, 100, -19, -45, 46, 25, -49, 79, -10, -1, 22, 75, 9, -50, 114, 106, -122, -89, 41, 1, 105, 123, -69, -123, 77, -61, -100, 15, -113, -19, 46, -53, 46, -89, -97, -38, 92, 73, 68, -101, 118, 67, 23, -17, 73, 109, 36, 76, 69, -10, 7, 64, -39, -49, -4, 3, -102, -15, 117, -8, -83, 6, 117, 105, 26, 28, 19, 66, 24, -47, -64, 86, 4, 57, 95, 23, 24, 76, -15, 106, -58, 77, -10, -112, -39, 55, -4, 95, -90, 61, 64, 32, 68, -43, -108, -15, -6, 63, -105, 72, -84, -10, -11, 122, 46, -84, 26, 76, -88, -67, -95, 10, 10, -89, -121, -65, -69, 112, 37, -106, 75, -94, -60, -7, -72, 44, 71, -108, -71, 31, 99, 9, 10, -68, -56, 69, 0, -71, -4, -87, -6, 83, 7, 108, 98, -37, -60, 16, 23, 26, 3, -119, -20, 58, 102, 29, 111, -43, 26, 37, 34, 9, 82, 76, 120, 7, 51, -35, 65, -93, 38, -82, -44, -31, 120, -93, 7, 10, -76, -12, 105, 41, 13, 123, -90, 57, 84, -123, -21, 49, 104, -103, -32, -79],numpy.int8)
        ca(self._r.i8_2, [-106, -119, 126, 87, 95, 79, -1, -15, -4, -30, 76, -121, 35, 80, 5, 7, -36, 102, 120, 105, 86, 98, 113, -62, 105, 38, 93, 20, 92, 7, -99, -121, -56, 50, -35, -95, 2, -43, -49, 73, 49, -42, -24, -3, -41, -59, 119, -108, 82, 98, 95, 111, 114, 115, 109, -125, -60, -45, -110, 31, -73, -111, 69, -108, -125, 14, -87, 61, 114, -104, -72, -67, 35, 26, 61, 59, -114, 125, -82, -34, 7, 71, -117, 125, 79, -116, -81, 3, -59, -121, 112, 64, 54, -9, -63, 37, -86, 104, -105, 7, 72, -99, 84, -3, -63, 77, 27, 36, 52, -110, 60, -119, -124, 82, -29, 107, 124, 105, 96, -34, -11, 0, 59, -39, -107, 55, 95, -26, -60, -30, -102, -94, -28, -7, 76, 56, -31, -68, 6, 101, 67, 101, -92, 120, 105, -119, 114, 6, 9, 43, 73, -64, -18, -77, -72, 84, -101, -114, -50, 28, 86, 103, -83, -109, -59, 82, 96, -70, 20, 75, -44, -3, -115, 60, 45, 94, 65, -108, 2, 12, 28, 110, -19, 20, 102, -41, 42, -61, -52, -54, 116, 114, -74, 14, -21, -43, -85, 16, 57, -62, -83, -79, 85, -7, 109, -45, 102, 28, 123, -96, 2, -37, -19, 104, 4, -43, -92, -114, 34, 44, 29, -96, -99, -95, -101, 12, 18, 107, 125, 114, -65, 126, -28, 114, -2, 9, 79, 69, 67, 78, -26, -95, 109, -81, 22, -61, 84, -16, -84, 57, 8, -88, -124, 119, 8, 35, -56, -14, -90, -73, 118, -4, -93, 35, -76, 6, -41, 98, -69, -108, -78, 16, -72, 43, -113, 71, -70, -51, -41, 62, -38, -58, 58, -127, 117, 67, 51, 34, -98, -13, -111, 13, 2, -101, -75, -22, 34, 42, -93, -106, 90, -65, -65, -82, 55, -111, -28, -114, 54, 0, 39, -46, 19, 78, 75, -116, 64, -120, -81, -116, -96, -36, 101, 67, -96, 14, 76, 74, 29, 67, 101, 68, -83, 62, 86, -64, -76, -87, 8, 44, -61, 31, 65, -120, 3, -82, 127, 105, 114, -58, -117, 52, -104, 117, 23, 4, -79, -44, -113, -65, 52, 83, 39, -120, 36, -80, 104, 46, 12, -61, 104, 99, 4, 53, 36, 91, 115, -8, -32, -111, 53, 6, 70, -70, 108, -68, 119, -3, -40, 110, -15, -94, 23, 36, -39, -87, 96, -89, -73, 119, 117, -45, -119, 48, -70, -28, -22, -127, -16, -56, -75, 72, 59, 54, -15, -57, -113, 78, -24, 63, 118, 74, -62, -101, 62, -123, 28, 0, -9, 30, 115, 47, 86, 88, -58, 91, 103, 121, 81, -78, 80, -50, -13, 33, 92, 107, -79, 55, -89, 34, -121, 82, -105, 59, 73, 59, 119, 72, -26, -122, 1, 41, 62, -11, -41, 101, -101, 79, 27, -73, -90, -2, -96, 10, 116, -86, -25, -117, -36, 13, -52, 90, -39, 113, -105, 71, -7, 2, 109, 106, 70, -86, -82, -121, 94, 58, 13, -124, 119, 34, 36, -37, 47, 23, -101, -96, -114, -37, -21, -37, -77, 121, -43, 25, -105, -6, 5, 3, -114, 30, -98, -74, -97, -43, 16, -84, -44, -56, 1, -115, -100, -46, -63, -100, 112, -106, -128, -2, -106, -116, -1, -43, -24, -73, -124, 14, 69, -90, 83, -85, -103, 52, 22, 58, -90, 77, -121, 110, 20, 114, -107, 102, -76, -6, -102, -38, 53, -100, -72, 118, -100, -113, 120, 53, -93, 61, -92, -84, -125, 81, 127, 125, -8, 99, 70, -49, -9, 86, 103, -96, -96, -40, 43, -48, 29, 28, 90, 45, -118, 111, -101, 24, -25, 123, -105, 124, 17, 27, -6, 111, -113, 21, -88, -117, 55, -7, -24, -24, 52, 39, -36, -81, 78, 95, 13, 121, -8, 116, -106, 45, -49, 19, 12, 13, -127, 109, -124, 14, 18, 84, -61, 23, 68, -102, 115, -34, 7, -10, 57, 107, -48, -53, -67, -63, -100, -84, -31, 79, -58, 56, 89, 40, 63, -37, 71, -7, -53, 91, -66, -74, -37, 48, -37, 123, -96, -11, -56, 80, -88, -53, 27, 7, -29, -124, -46, 22, -103, -67, 93, 42, -37, 18, -126, 120, -81, 74, 26, -54, 19, 86, -112, -38, -57, 119, 26, -62, -67, 126, -50, -31, -36, 120, -127, 123, -88, 43, 50, 61, 94, -80, 35, 41, -109, 71, 91, -118, 66, -60, -127, 47, 75, -52, -66, -125, -111, 44, 116, 9, 68, 115, 113, 8, -4, 39, 23, 54, 107, -119, 1, -68, -11, 103, -123, 29, -92, 15, -10, -31, 35, -91, 38, 37, 110, 9, 80, -115, -120, 112, 110, -28, -116, 63, 85, -65, 5, 122, 19, -84, 97, -16, -46, 97, 104, 28, -83, -33, 38, -18, -8, -126, 82, 81, 88, 109, 118, -56, 64, -96, 36, -10, -109, 74, -86, 105, 123, 110, -116, 91, 15, 123, -26, -121, 75, 63, 24, 94, -43, 123, 74, 79, -42, 74, -102, 57, -27, 116, 126, -100, 2, 49, 17, 28, 27, -58, -98, 39, 50, -66, -75, -23, -112, 64, -16, 60, -62, 122, 53, -42, 21, -40, 88, 2, 62, -103, 108, -74, -95, 113, -49, -73, 63, 94, 44, -41, -68, -124, 46, 13, -17, 11, -100, 58, -98, -40, -64, -56, 21, -47, -120, -7, -23, -51, 27, -99, -42, -109, -55, 106, 92, 110, 19, 32, -117, 4, -34, 65, 72, -100, -122, -69, -94, 122, 60, 23, -93, -84, 30, 118, -92, 88, -104, 23, -71, 115, 106, -118, 9, 64, -34, -71, 43, -92, -13, -82, -5, 15, 18, -11, -113, -109, -128, 104, 34, 72, -110, -59, -113, 69, -106, -74, -66, 115, -31, -27, 59, -73, 73, 120, -34, 59, 126, -93, 49, -53, 114, -122, -28, -28, 94, -37, -90, -32, 80, 15, 4, -101, -78])
        self._r.u8_1 = 232
        if self._r.u8_1 != 222:
            raise Exception()
        self._r.u8_2 = numpy.array([52, 40, 13, 185, 137, 3, 173, 236, 60, 18, 206, 224, 231, 19, 31, 139, 177, 201, 100, 37, 8, 94, 145, 135, 217, 32, 59, 26, 243, 213, 97, 78, 145, 136, 142, 249, 46, 247, 20, 240, 47, 211, 60, 35, 170, 0, 119, 14, 36, 7, 165, 132, 35, 199, 33, 45, 27, 111, 135, 50, 210, 248, 118, 162, 199, 152, 28, 202, 222, 8, 191, 40, 134, 213, 36, 131, 198, 76, 82, 212, 26, 33, 219, 181, 213, 205, 104, 118, 74, 239, 226, 65, 161, 29, 158, 223, 175, 214, 160, 65, 229, 56, 207, 64, 194, 167, 85, 221, 82, 56, 182, 226, 206, 71, 203, 116, 201, 234, 16, 42, 32, 47, 149, 161, 173, 60, 195, 59, 138, 241, 52, 152, 48, 57, 137, 206, 201, 58, 242, 139, 149, 42, 185, 94, 27, 224, 249, 33, 24, 18, 148, 104, 89, 163, 94, 214, 232, 133, 74, 124, 117, 39, 0, 73, 86, 254, 186, 224, 96, 236, 113, 39, 28, 245, 218, 147, 215, 62, 191, 23, 20, 27, 32, 151, 25, 225, 3, 157, 221, 133, 124, 35, 41, 177, 93, 137, 198, 96, 129, 235, 21, 10, 110, 16, 25, 65, 153, 157, 139, 82, 24, 43, 4, 180, 238, 174, 226, 183, 56, 224, 239, 130, 62, 40, 12, 226, 219, 164, 71, 242, 179, 227, 53, 148, 38, 228, 151, 2, 249, 132, 56, 253, 10, 107, 241, 56, 97, 88, 198, 203, 33, 132, 212, 44, 239, 7, 206, 156, 144, 93, 44, 71, 40, 171, 60, 234, 89, 238, 114, 240, 145, 141, 51, 180, 85, 75, 125, 219, 2, 121, 53, 12, 223, 90, 174, 248, 45, 39, 151, 5, 155, 29, 244, 124, 156, 60, 250, 52, 54, 186, 95, 245, 18, 51, 52, 183, 105, 226, 245, 214, 94, 254, 98, 14, 46, 203, 225, 95, 126, 178, 49, 82, 159, 231, 170, 250, 63, 162, 156, 218, 184, 211, 76, 181, 97, 180, 239, 45, 135, 147, 49, 147, 0, 32, 22, 77, 209, 215, 54, 83, 29, 127, 80, 150, 50, 15, 69, 33, 118, 255, 168, 201, 2, 218, 13, 53, 164, 101, 34, 218, 110, 107, 147, 5, 78, 135, 1, 11, 242, 43, 181, 108, 107, 46, 176, 74, 2, 251, 26, 97, 254, 79, 204, 97, 41, 90, 126, 81, 202, 70, 30, 70, 50, 25, 56, 249, 245, 159, 6, 102, 21, 85, 8, 94, 115, 88, 32, 33, 111, 138, 229, 238, 152, 198, 74, 111, 86, 151, 165, 232, 2, 13, 42, 228, 219, 158, 227, 203, 47, 8, 83, 139, 184, 165, 123, 55, 29, 198, 119, 78, 182, 200, 77, 8, 5, 135, 164, 82, 235, 210, 47, 105, 53, 186, 64, 197, 24, 14, 39, 161, 187, 136, 58, 118, 225, 162, 203, 5, 214, 155, 45, 3, 111, 126, 99, 196, 82, 14, 156, 165, 134, 83, 179, 5, 226, 237, 151, 0, 219, 251, 160, 239, 224, 133, 230, 237, 221, 233, 12, 3, 189, 28, 251, 245, 89, 116, 113, 176, 40, 210, 216, 173, 154, 216, 111, 254, 183, 238, 29, 85, 142, 189, 89, 235, 184, 241, 2, 99, 138, 222, 47, 128, 97, 235, 195, 106, 118, 196, 149, 53, 188, 70, 113, 85, 90, 53, 179, 32, 23, 28, 95, 164, 49, 61, 151, 70, 214, 245, 245, 117, 172, 75, 153, 117, 226, 69, 205, 173, 139, 140, 163, 107, 214, 18, 111, 194, 115, 236, 32, 239, 168, 62, 12, 207, 220, 162, 160, 13, 147, 252, 192, 145, 150, 207, 112, 196, 114, 88, 69, 252, 193, 37, 84, 103, 108, 32, 205, 224, 216, 206, 251, 185, 17, 55, 185, 112, 24, 8, 209, 184, 156, 65, 48, 196, 236, 45, 97, 65, 218, 239, 59, 191, 137, 3, 182, 135, 46, 142, 163, 39, 63, 219, 66, 166, 8, 41, 175, 79, 77, 134, 159, 149, 118, 63, 191, 86, 103, 32, 2, 239, 107, 199, 122, 148, 93, 252, 176, 112, 130, 88, 102, 225, 199, 89, 100, 221, 177, 118, 102, 77, 192, 224, 117, 13, 213, 164, 87, 91, 157, 211, 14, 248, 15, 0, 165, 101, 185, 228, 203, 227, 44, 157, 68, 34],numpy.uint8)
        ca(self._r.u8_2, [20, 34, 154, 240, 82, 27, 230, 242, 253, 161, 17, 124, 80, 120, 210, 237, 179, 95, 224, 104, 74, 77, 148, 17, 98, 7, 13, 203, 155, 197, 223, 36, 207, 87, 56, 56, 76, 112, 100, 154, 40, 239, 13, 185, 77, 91, 107, 73, 196, 234, 3, 235, 40, 222, 224, 46, 47, 150, 167, 104, 206, 245, 20, 181, 133, 190, 255, 1, 183, 218, 5, 121, 233, 68, 72, 140, 250, 213, 199, 143, 41, 22, 238, 149, 235, 42, 170, 2, 58, 242, 91, 116, 62, 167, 113, 28, 8, 0, 199, 142, 8, 102, 60, 87, 147, 104, 125, 163, 135, 1, 186, 44, 117, 103, 186, 50, 68, 179, 203, 61, 231, 80, 45, 35, 231, 127, 93, 49, 154, 182, 1, 151, 111, 70, 127, 13, 41, 113, 170, 41, 173, 14, 129, 108, 235, 166, 153, 50, 203, 42, 43, 93, 243, 114, 190, 225, 12, 227, 24, 221, 177, 188, 218, 55, 6, 199, 162, 67, 152, 185, 216, 108, 251, 225, 146, 85, 220, 192, 36, 39, 20, 189, 24, 117, 98, 107, 215, 238, 145, 113, 40, 184, 110, 186, 66, 207, 164, 43, 70, 242, 211, 65, 232, 92, 164, 178, 3, 120, 1, 28, 247, 234, 210, 20, 61, 83, 147, 174, 177, 131, 229, 117, 211, 161, 73, 161, 224, 80, 219, 151, 131, 42, 37, 46, 68, 213, 62, 101, 8, 143, 146, 103, 52, 69, 7, 241, 55, 191, 104, 208, 100, 192, 48, 199, 30, 38, 148, 25, 252, 47, 18, 152, 142, 181, 231, 205, 166, 171, 14, 236, 15, 232, 235, 36, 66, 88, 141, 87, 66, 9, 94, 214, 100, 227, 207, 1, 6, 102, 170, 53, 53, 152, 136, 115, 251, 227, 218, 164, 20, 109, 174, 36, 135, 122, 237, 146, 226, 42, 202, 183, 112, 68, 121, 92, 23, 75, 34, 228, 131, 141, 52, 12, 132, 12, 43, 220, 33, 110, 30, 120, 244, 192, 128, 190, 89, 109, 165, 9, 25, 27, 129, 135, 80, 17, 217, 152, 237, 241, 56, 233, 78, 224, 115, 143, 214, 201, 78, 139, 50, 185, 115, 234, 31, 11, 190, 244, 28, 93, 13, 153, 78, 154, 62, 86, 40, 133, 29, 12, 133, 69, 50, 197, 127, 242, 14, 173, 70, 116, 243, 200, 197, 245, 249, 231, 139, 46, 99, 37, 55, 220, 57, 103, 163, 71, 252, 54, 52, 254, 97, 158, 155, 249, 243, 55, 112, 226, 88, 25, 29, 41, 109, 6, 219, 193, 89, 193, 164, 166, 103, 119, 69, 214, 105, 14, 20, 208, 56, 231, 59, 68, 49, 107, 119, 99, 109, 210, 234, 228, 111, 219, 32, 211, 172, 101, 172, 99, 227, 112, 137, 204, 19, 3, 111, 219, 245, 89, 106, 32, 108, 234, 81, 72, 27, 99, 151, 212, 108, 37, 248, 183, 241, 194, 37, 73, 230, 130, 11, 6, 122, 220, 192, 114, 116, 208, 187, 159, 226, 98, 191, 253, 226, 39, 212, 138, 106, 196, 153, 61, 218, 218, 20, 238, 82, 237, 196, 114, 135, 239, 221, 20, 52, 73, 208, 234, 99, 185, 218, 218, 47, 95, 218, 110, 165, 216, 121, 249, 203, 206, 213, 201, 138, 253, 43, 238, 131, 62, 229, 123, 69, 175, 61, 176, 180, 72, 120, 158, 91, 145, 16, 162, 70, 54, 170, 170, 60, 9, 226, 40, 66, 159, 139, 83, 20, 171, 32, 189, 140, 122, 1, 64, 144, 250, 94, 74, 91, 160, 146, 146, 17, 78, 43, 115, 166, 63, 81, 88, 83, 178, 177, 110, 93, 188, 29, 41, 28, 73, 40, 245, 49, 63, 134, 103, 135, 17, 172, 150, 249, 23, 230, 166, 31, 55, 203, 149, 19, 4, 101, 237])
        u8_3_1 = numpy.array([66, 135, 166, 109, 89, 156, 182, 63, 217, 36, 212, 158, 7, 212, 235, 154, 155, 52, 234, 220, 30, 251, 223, 77, 163, 204, 220, 63, 152, 39, 193, 217, 212, 4, 248, 69, 117, 164, 83, 149, 60, 44, 96, 78, 166, 212, 56, 87, 183, 20, 0, 32, 244, 16, 155, 4, 82, 217, 235, 203, 171, 188, 222, 15, 0, 109, 97, 135, 62, 185, 103, 39, 200, 198, 50, 190, 246, 161, 102, 32, 246, 11, 26, 132, 145, 141, 15, 112, 193, 105, 130, 61, 177, 104, 39, 164, 188, 131, 6, 9, 222, 109, 161, 211, 254, 73, 117, 59, 96, 146, 92, 148, 175, 82, 108, 215, 210, 4, 7, 176, 191, 129, 174, 224, 139, 166, 71, 30, 57, 246, 94, 139, 121, 190, 210, 181, 44, 71, 7, 118, 76, 223, 173, 181, 88, 138, 18, 146, 233, 135, 205, 101, 92, 222, 136, 177, 15, 167, 154, 198, 194, 185, 166, 21, 49, 193, 229, 153, 231, 101, 47, 40, 181, 138, 207, 168, 73, 19, 108, 15, 22, 193, 101, 151, 216, 153, 20, 140, 209, 15, 117, 246, 86, 210, 193, 254, 56, 41, 223, 107, 179, 130, 220, 46, 248, 200, 241, 173, 67, 147, 93, 87, 108, 13, 180, 112, 58, 210, 243, 94, 113, 140, 172, 53, 206, 186, 106, 167, 48, 43, 213, 157, 135, 243, 72, 173, 185, 62, 188, 162, 61, 19, 156, 215, 24, 216, 222, 56, 211, 151, 178, 251, 238, 47, 51, 141, 109, 214, 179, 41, 5, 190, 79, 27, 13, 208, 37, 97, 178, 83, 150, 77, 187, 179, 12, 73, 156, 167, 167, 106, 198, 157, 133, 80, 183, 15, 1, 204, 84, 250, 122, 232, 178, 103, 225, 110, 97, 23, 171, 88],dtype=numpy.uint8).reshape([30, 10],order="F")
        self._r.u8_3 = u8_3_1
        u8_3_2 = self._r.u8_3
        ca([10, 20], u8_3_2.shape)
        ca(u8_3_2.flatten(order="F"), [23, 5, 170, 52, 174, 242, 108, 186, 30, 27, 38, 181, 184, 103, 240, 129, 69, 179, 148, 194, 57, 7, 19, 111, 244, 86, 238, 36, 31, 44, 193, 106, 229, 159, 23, 70, 184, 121, 243, 215, 187, 115, 89, 141, 233, 105, 150, 224, 245, 251, 44, 148, 149, 123, 141, 9, 77, 17, 146, 157, 112, 122, 83, 50, 156, 178, 186, 244, 234, 165, 6, 223, 148, 48, 189, 46, 209, 30, 203, 186, 4, 159, 162, 97, 97, 232, 113, 178, 244, 172, 54, 52, 252, 32, 35, 131, 178, 21, 131, 165, 203, 113, 141, 3, 195, 54, 143, 163, 15, 99, 29, 235, 125, 45, 50, 157, 255, 7, 81, 221, 70, 225, 119, 220, 98, 55, 213, 23, 219, 152, 148, 113, 89, 236, 109, 187, 7, 80, 140, 226, 71, 34, 17, 176, 15, 30, 239, 251, 10, 64, 170, 150, 245, 180, 83, 242, 138, 154, 226, 193, 119, 43, 85, 164, 187, 73, 19, 81, 119, 168, 160, 222, 100, 230, 27, 237, 43, 71, 144, 132, 212, 131, 241, 195, 181, 175, 41, 115, 149, 128, 238, 212, 134, 110, 224, 149, 217, 213, 122, 200])
        self._r.i16_1 = 2387
        if self._r.i16_1 != -13428:
            raise Exception()
        self._r.i16_2 = numpy.array([-29064, 7306, 1457, -19474, -671, 22876, -14357, -18020, -23418, -10298, 1040, -2415, -22890, 4293, 25366, 12606, -31678, -15908, -11164, 20643, -239, -15149, 25272, 17505, 24037, 8264, -3888, -12405, -28698, 25222, -2506, -26405, 9561, 27093, 8022, 23338, -31489, 24117, 18018, 25324, -22192, -23413, -12544, -29675, -10752, -7108, 3021, 29238, -10332, -1818, 23363, 31568, -15057, 9565, 30520, 1064, 26637, -29070, 11149, 8534, -13775, -18359, 9626, 10662, -23713, 28470, 8840, -25279, 18175, 13675, 14955, 30323, 924, -13113, -21483, -6641, 12790, 26367, 27907, -1062, -24249, -13215, -18475, -11121, 2339, -2361, -7790, -26038, -6984, -10142, 8485, 17258, 6150, -25530, 9655, -11378, -805, 11574, 16094, 21091, -11882, 21514, 27655, -27624, -23592, 17985, 3154, -1292, 11059, 27599, -2741, -27514, -27353, -1824, -26419, -19633, 23008, 22184, 25855, -4965, -18710, -6802, 25237, -24262, 3253, -28401, -19864, -11711, -27668, 28671, -1376, -8600, -12691, -18972, -5265, 3901, -6694, 19018, 29612, 8047, -26257, 28662, -6164, 9407, -12556, 1421, 14531, 28000, 8499, 5512, 28989, -17181, -4051, 28130, 19063, 31736, -28399, -4663, 25520, -18490, -32156, -15267, 29245, -13510, 13446, -31039, 18030, 25419, 24594, 28348, 17845, -26123, 20713, 29810, -25881, -10534, 9038, -15614, 20117, 11436, 7078, 9985, -2758, -13790, 12865, -6824, 10924, -4750, 10127, -30953, -15114, -10407, 13061, -13241, 22268, 15514, -23952, -22361, 25465, -23395, -5885, 23643, 6634, 1768, -4390, -29064, -18261, -18954, 22866, -23739, -15996, -31521, -12816, -11246, -16029, 4113, -18809, -4282, -3892, -21196, 23692, 6488, -8949, 28859, 23717, -20358, -4216, 6700, -14565, 14268, -17978, -3865, 21937, 17864, -26293, -9181, 28460, -27725, -32278, -13856, -21763, 10310, -4066, 32078, -8132, -14677, -11698, -23123, -30968, -21889, -2192, 29299, 623, -26725, -29380, -18038, -25037, 26361, 22773, -31157, 22096, 10336, 26530, -74, 3820, 52, -28257, -29110, -29891, -23752, -23846, -15516, -21528, 14792, -4286, 26942, 17922, 21495, 16249, -30305, 3056, -22525, -4198, 28613, 2695, 30388, -18066, -5162, -23655, -25604, -28244, -1196, -6888, 17903, 11721, 13555, 32445, 31800, 11125, -31537, 1400, 25992, 2289, -19330, 29486, -27986, -6690, 9402, 15366, 18268, 29476, 27543, -26894, 28279, -18810, -14493, 6622, 9548, 28691, 30421, -17983, -25525, -6167, 5825, -25283, 19498, -17719, -3858, 8518, 16017, 1325, -16864, 17874, -796, 3678, -32078, -19712, -32173, -25895, 27397, 23474, 10508, -6009, 25388, 17327, 26954, -23909, 27502, -15956, -1770, 1343, -30108, -12923, -3584, -30762, 3386, 18090, -14048, 31833, -5312, -32483, -1358, -28372, -24388, -26718, -17132, 22775, 16924, -8991, -12343, 16874, 19515, 21977, -26287, -28976, -18071, -24572, -8740, 29859, -21779, -20087, -928, 31016, -11442, 16890, -12445, 26140, 23581, -18737, 16033, -16426, -27860, -4853, 6669, -2678, -14760, 15011, 25458, -24354, -4704, 1983, 20655, -3885, -6015, -20382, -6168, -8801, 21318, 21969, 15333, 26667, -15860, -20356, -4265, -19871, -30123, 8082, -5186, -5294, -7119, -23580, 600, 7195, 24630, -9810, -23846, 23416, -26102, 11875, 25362, -17002, 32482, 3733, 8434, 18377, -11770, 21843, -19779, 27194, -16918, -22013, 8387, -1686, -27228, -8013, -12979, 30682, 13008, -32188, 24547, 27126, 12811, -14996, 16305, 16467, 21204, -16620, 20671, 31564, -23123, -31995, 6335, -26234, -8852, -19185, -19636, -15411, 22541, 10295, -14022, -19669, 25371, 4407, -21395, -20754, -31164, -30944, -29004, -28877, 11049, -11492, 30171, -3452, 20020, -30618, 11178, 7734, 15658, 26485, -8697, 24391, 14520, -9994, -11594, 21221, 21327, 22058, -6275, -2272, 20061, 11315, 26569, 21368, 30729, -15573, -25453, -6160, -20236, -29377, -22591, -11045, 19992, -18369, -30261, -32159, 27646, 18350, -6134, 6723, -13437, -23761, -22496, -12447, -1184, -17634, -20936, 30815, 32042, 10621, 17252, 9705, 4169, -8075, -20113, -21095, -20310, -3917, 23438, -1628, 7291, -18739, -12603, 22036, -14198, 26960, -24387, -20204, 1370, -23683, -27522, 31684, -24806, -20567, 606, -14584, -5656, -6025, 20297, -18716, -7075, 21089, -26036, -2747, -18800, 22214, -31288, -31916, -32543, 14577, -6407, 17079, 4683, -29301, -13707, 4296, -2247, -25994, -322, -26904, -4444, 24454, -9676, 29589, 30545, 17995, 20596, 24835, 24545, -15782, 13901, -26644, 4655, -10543, -24521, 30118, -29985, 3163, -27379, 24263, 19271, 12184, 7695, -6249, -26163, -16952, -18930, -22627, 5625, -16862, -29626, 8000, -26542, -21846, 8377, -6837, -30324, 10752, 19676, -31224, -11472, 27419, 4926, -67, 7107, 3149, -18440, 18652, -32124, 26094, -7015, -10179, 3878, 28709, 4453, 20330, -27548, -18729, -7550, -29815, -3110, -14705, -16383, 16020, 15466, 5411, 23434, -14919, -1289, 24403, -2409, -28824, -5982, 21794, -26131, 11683, 28742, -21742, 7952, -9041, 28373, 12434, -17665, -19141, -31576, 650, -11103, -26587, -17144, 20830, 1468, 23981, -6189, -1574, 11151, 9314, 12189, -19801, 23310, 3132, 1145, -5231, 1387, 3230, -15314, -17253, -29867, 22979, -28009, 7686, -31739, -16295, 23702, 9141, 18300, 31485, -11124, -30999, -26289, -32371, 7900, -5057, -8202, -15209, -26424, -2712, -25152, -7174, -25019, -14712, -10703, -2809, -9, -17905, 20882, 31301, 8989, 20139, -235, 707, -23246, 4519, 5621, 9609, -10846, -1873, -17425, 30184, 23010, 18718, 24429, -2168, 23884, -19503, 9419, -24927, -16803, 11872, 16572, -30227, 4356, 18692, 3493, -29119, 16296, 1632, 8736, 7806, -13904, -26360, -27538, 6861, -8093, -6184, -445, -2181, -9581, -2722, 22857, 4100, -2585, -25935, -26353, -21284, 7497, -5385, 10974, -7747, -19865, -1205, -12806, -7505, -29792, 16793, -2743, 30123, 9379, 17381, 4947, -15940, -3652, -1797, 21012, -10333, -27953, -1716, -28455, 29598, 17497, -5363, -3990, -29921, -27210, 8825, 8046, 11062, -13647, 29708, 1335, -22559, -28213, -9634, -17768, 32543, -15641, -18576, -23375, -25305, 11930, 11338, 28057, 12085, -17504, 29366, 3513, 26451, 29229, -24338, 1541, 18497, -8424, 12969, -20692, -24323, 1876, 8233, 10893, -10761, -3855, -21938, -6268, 32120, -25120, 20729, -371, 25746, 28224, -25625, -22924, -30667, 13100, -3160, 28610, 2206, 977, -17607, -2173, 24212, 14451, 22276, 26268, -10890, -23818, 30052, -18695, 14828, -16839, -18543, 17056, -3715, -7372, -16029, 31885, -20617, 10847, -12068, 29898, 12865, 30922, 17546, -8489, 19324, 584, 9798, 2421, -17432, -10905, -14728, -7920, 6909, -11895, 1031, 18387, 20783, -28969, -535, 31095, -30709, 28734, 15322, 28585, 2100, -6234, -28704, -2813, 22201, 16682, -1576, 9351, 30508, -9447, -21309, 3023, -19963, 13739, 8398, -11148, -9348, 32285, -22925, 697, -9683, -1106, 11252, -16321, 31326, -22577, -107, 3355, 22765, -10391, -26902, 10375, -2846, -21378, 2649, 1284, 23016, 6884, -5356, -17352, -9866, -4313, 15950, 12058, -32753, 6124, -9833, 8828, -11711, -28691, -31249, -31354, 13039, 29161, -17382, -5879, -21118, 11736, -29024, -15440, 9364, 28121, 16093, 20123, -26504, 25957, 11858, 9932, -11333, -15770, 3678, -18107, -25852, -21244, 2225, -13899, 2050, -21656, -7352, -3896, 4161, -27416, 12792, -1807, 18088, -9590, 1851, -11661, -28665, 10986, 18137, 22612, -1617, -11139, 19293, 4080, 8597, -16998, 17228, 6587, 12316, 12640, 1001, 25972, 29637, 27715, 5577, -12737],numpy.int16)
        ca(self._r.i16_2, [-31396, -31525, 21618, 420, -4709, -28067, 13158, 30433, -5226, 177, 32486, -24906, 14134, -12316, 815, 14221, 25078, 4427, -24570, -2404, 32275, 16625, -18211, 8224, 11466, -8053, 25673, -5521, -3629, -28951, 16888, 3476, 29692, -16313, -6124, 7022, 20178, 363, -26079, 6451, 26271, -9454, 7484, 9626, 18076, -32556, 8132, 22992, -22922, 21831, 9586, 30404, -24016, -22082, 17247, -120, 26786, -30338, 6445, 7710, 12192, 1787, 10373, 8221, 9130, -13265, -29233, -30762, 1430, 29737, 1503, 32216, -27766, 25651, 24365, -20157, 18077, -9909, -2427, -14841, -32092, 2606, -29807, 31676, -2674, 21400, -31068, -7881, 15682, -5497, -4695, -7670, -26719, 7180, 31393, 20250, -18099, 12591, 18352, 16854, 24663, -12445, 3967, 13535, -9324, -28110, 13977, -23172, 14216, 30378, 6653, 19203, 7298, -23065, 18301, 27111, -23775, -27934, -4797, 22319, -5834, -10073, 21636, 26423, 20007, -23826, 9433, 24251, 29231, 26264, 2698, -10085, -21536, -27028, -24687, -3768, 1511, 25182, 29258, -17177, 8345, 9571, 7512, -28872, 10123, -10644, -7612, -13232, 24346, -25900, 28049, -5366, -8968, 5589, -21840, 21891, 25327, 9095, 4382, -30532, -21172, -27251, 12320, 30065, -29933, 19371, -5654, 7815, -26289, 12614, 13834, 29357, 25201, -32309, 20042, 16706, 2312, -20975, -5346, 1820, 9166, 20644, -3811, -12569, -3711, 11580, -24719, 29072, -26433, -12475, -15326, 1071, 10750, -17120, 21953, 11265, 3513, 20747, 32085, 9898, -24426, -17231, 21523, -26126, 8783, 31762, 6629, -32554, 28071, 23409, -6423, -25261, -13387, -2606, -23878, 5003, -8970, 16999, -11501, 15402, -31573, -12730, 17823, 3018, 13959, 6305, -24676, -28537, -21613, 15353, -31686, 7264, 14978, -2702, 25179, 16061, -5220, -20419, 17023, -5104, -17836, -24537, 30832, -8236, 20473, 31052, 9467, 25660, -4882, 28392, -16236, 15059, 18409, 2709, 9637, -28754, -28261, 14474, 281, 24844, 25464, 26378, 8331, -8080, -10826, -3874, 21290, 1599, -375, 8436, -25280, 25907, 19361, 6448, -26639, -15164, -12896, 1476, -15877, 23427, -24851, -23147, -11525, 16456, -23417, 31519, -10431, -14222, -28958, 6194, -7802, 17086, -5885, 23977, 29347, 3648, 29674, -27985, 1834, 30677, -30455, 32438, -23495, -10403, 10370, 32713, 27187, -4733, -16686, -21336, 7793, 15123, 17046, 28022, -23346, 21816, 16826, 19747, 21625, 17895, -23683, -142, -27996, 6601, -13889, 24112, -19505, 24425, 11673, -3507, -9946, 20693, -28974, -30639, 25202, -24295, 27916, 5920, 17325, 29121, 12475, -1179, 5379, -21558, -8684, 7551, -8536, 8673, -13435, -3870, -6389, -26193, 13662, -17405, 3305, -15401, -10014, 6645, -9322, -15604, 7511, -8894, -2421, -21984, -12209, 16631, 19022, 11644, -3624, 25297, 6613, 4801, -17413, -12780, -28095, 17986, 11066, 22207, 17717, 3613, 14987, -19860, 12693, -13482, 10471, -24561, 32333, -25968, 7244, 7005, 17820, -18897, 13208, 16753, 32551, 21296, -15046, -3886, -13628, -2550, 16059, 1090, -27901, 21254, 21726, -17180, 5902, 30053, 31909, 25120, 3958, 18119, -25501, -4974, -11464, 24068, 19720, -8793, -9011, -11975, 7025, -15041, 21009, -15123, 3647, -28657, -7700, -10174, -16814, 4848, 13044, -20100, -17977, -29197, 31169, 15459, -27346, -23297, 1639, -27165, 25474, -4981, -16728, 24962, 6895, 16619, 12965, 10990, -13275, 1119, -10243, 10364, 3763, 3565, 31542, -22261, 15267, -31448, 13298, -8408, 511, 19296, 24390, -25118, -29033, 11413, 25520, -23675, -12986, -3952, 7133, 9587, 30652, -21444, 23859, 22577])
        self._r.u16_1 = 54732
        if self._r.u16_1 != 60981:
            raise Exception()
        self._r.u16_2 = numpy.array([27153, 43996, 41432, 58304, 12942, 58876, 28186, 11185, 10827, 17769, 13091, 23017, 17671, 49113, 6987, 35547, 2024, 33499, 26956, 11772, 20498, 42863, 65021, 31883, 61940, 6622, 59235, 6137, 51350, 48773, 57425, 56027, 38431, 12927, 54445, 12445, 27087, 33727, 51305, 48371, 7488, 32356, 59057, 10185, 57955, 46571, 326, 43692, 43661, 25990, 42979, 8957, 59425, 9205, 42414, 10752, 5573, 37965, 14726, 60329, 24708, 38900, 13804, 12531, 19400, 40437, 3102, 15384, 9922, 48890, 655, 58588, 55933, 56542, 20001, 11584, 62303, 19888, 38565, 19636, 21974, 26170, 61468, 27655, 30144, 38002, 59044, 33839, 58996, 7516, 41660, 26146, 20606, 9052, 41933, 43479, 45221, 37564, 60731, 9073, 5647, 25184, 21426, 47334, 48473, 57336, 38775, 56475, 55863, 33194, 59184, 17109, 10792, 35915, 37682, 18123, 56383, 55538, 26718, 29128, 5521, 51803, 22632, 19827, 32242, 38280, 51359, 10800, 22661, 63621, 58920, 22073, 59845, 56670, 24860, 21801, 22225, 45849, 35453, 38351, 58831, 63677, 49340, 58625, 59284, 8244, 22567, 42599, 39629, 44023, 55480, 23933, 54557, 36080, 18074, 53598, 26233, 46291, 10356, 982, 20899, 9791, 43246, 40308, 38630, 40376, 23805, 35194, 45957, 56662, 38493, 50650, 41811, 40225, 20212, 10975, 38947, 14443, 62213, 16366, 55641, 20063, 28304, 34336, 48695, 11196, 20382, 32670, 61020, 27154, 60750, 42124, 64065, 45687, 32335, 60310, 14344, 39059, 31190, 12119, 57101, 13774, 58824, 54012, 32689, 12347, 13368, 42262, 15453, 61631, 51804, 27658, 53000, 30414, 42427, 61957, 16811, 19230, 23527, 24728, 60773, 28925],numpy.uint16)
        ca(self._r.u16_2, [28720, 34616, 62158, 23483, 4737, 55943, 56769, 39984, 64598, 51111, 51377, 21150, 23557, 7441, 55455, 37627, 34814, 32887, 12525, 7947, 30317, 19555, 62568, 26666, 35231, 38385, 56455, 37676, 47722, 60644, 1037, 61159, 64542, 21655, 57027, 46262, 64919, 49927, 25520, 56784, 4424, 62463, 26885, 43771, 5149, 7537, 28615, 2661, 41921, 63221, 30209, 37930, 9683, 52406, 24968, 50022, 51469, 57731, 65408, 57019, 62539, 10550, 35726, 34413, 46756, 63743, 50854, 1075, 36709, 52737, 38989, 14194, 10541, 39864, 7632, 6335, 37317, 18084, 18417, 13903, 41588, 4410, 55813, 34564, 62937, 56211, 51771, 32961, 36295, 58221, 4107, 18571, 55106, 52625, 36243, 52487, 10236, 36619, 24439, 41204, 61791, 12156, 5380, 26272, 45613, 37851, 60070, 38759, 33502, 2147, 28146, 45977, 51698, 33640, 38956, 48664, 51750, 42329, 6020, 42645, 44393, 47459, 64398, 2683, 18251, 5304, 38780, 13706, 58825, 12565, 37762, 21280, 39402, 56275, 25627, 41371, 39366, 61829, 8892, 26779, 311, 47322, 26823, 8265, 12495, 38802, 20059, 32724, 7618, 37557, 57579, 33492, 20655, 19185, 57872, 51794, 16721, 52071, 52584, 57226, 28584, 9690, 10117, 41708, 38496, 56164, 53099, 45246, 34962, 41133, 9780, 39381, 53780, 14719, 64870, 38034, 15484, 24376, 39802, 58424, 52906, 45995, 50396, 21981, 32813, 15889, 33981, 58999, 48157, 23717, 24644, 18059, 47204, 45872, 26705, 46193, 56697, 41192, 56316, 43920])
        self._r.i32_1 = -9837284
        if self._r.i32_1 != 898734:
            raise Exception()
        self._r.i32_2 = numpy.array([-966485083, 547919123, -1194190604, 1550099195, -86896479, -1346998266, -111775936, 1595883280, 95277373, -483593724, -1194231658, -1664247993, -1125879490, -774112094, -908971354, 1257430739, 278831106, 2146175077, 1216734947, 108534888, 712376825, 472415212, -413092215, -186896831, -983274891, -814159203, 491332674, -1080086896, 305863740, -588641755, -1173634854, 1500595228, -1011735210, 1396816521, -1843412764, -1174697157, -2042333138, 1720132956, 1179474025, -734588992, 1928960553, 653905969, -1152761709, 206317133, 1066603916, 1788908206, 1901091544, 1610435338, -1051581785, -1953636422, 1076388567, 1462395490, -237116033, 454691362, 1619801391, 1845599647, 1868321380, 1723200218, 766619638, 105371815, -877177590, -1885723170, 434710859, -1146593520, 209995917, -1047842747, 465673729, -2084508649, 1968279245, 587205365, 1583233886, -1752333729, -114021301, 59161723, 1580036234, 345745650, -468378351, 245003371, 1673787261, 1587452615, -1303597866, 822157520, 64527339, -4281296, -64380840, 37142322, 500059241, -1469346913, 11916922, -338760031, -2025817128, 83726551, -754215578, 368103720, -821582629, 717962460, 2144471201, 223671109, -199755353, -841621639, 1540857720, 1804628518, 2118963299, -1595232224, 400238135, 933224750, -215585205, -985264044, -988901458, 986847698, -1856650438, -651146661, -978168494, -532172509, 1691932093, 1876106029, 525396768, 1743090554, -162073951, 806798458, -1403694340, 559542160, 207806919, 590536881, -1650417281, 1858408059, 1983218923, -1543131382, 1706115652, 2119926306, 1424134413, 1205448675, 1811525641, 861875958, 2007619106, -845489490, -55633190, 1816674890, -614507920, 286578932, -1342898663, -1261324825, -1506404786, -1806499804, 1974771054, -98303714, -290587554, 1090231453, -985937256, -839357172, -1416681172, -1007624128, -1578990962, -1728169897, -844916635, 506302833, 667662716, -663874058, -1362455403, -2060230793, -1319792032, -2017894569, -1689519196, 479605380, -117340189, -1052087080, 1498560347, -870303564, 1098382715, -2086046098, -1642542296, -628648039, -719920250, -2060321401, 525438216, 281529006, -459505556, -1796557506, 1024549346, 1853853925, -312303325, -1579857332, -1269984071, 473304768, 721731410, -1737559733, -438494623, 1802127802, -1731233704, -1390726345, 485787940, 943002107, -187237495, 1869312126, 442020547, -87826467, -696183927, 616713843, 945472556, -972856985, 151686386, 1488133092, 175341883, -1180397098, 948926458, -503479659, -1267580010, -388943415, -1363469783, -1527776457, 268299441, 191219066, -1024035842, -1475980660, 1828759673, -1442955646, 1790351422, 574018056, 1803848768, -2095818881, 1210053959, 1551296999, -942626269, -1321443296, -1859662526, -2071020753, -1184904851, 988848078, -412054768, 1493935320, -196557049, -704875093, 134497249, -1224190928, -2068208534, -965095455, -564081208, -1156543555, 461090533, 701882132, 910649700, -1878641070, 1446533896, 1970740772, -204663013, -1698033554, 972688594, 1110078968, 810548960, -1509538061, 1958800693, -543420990, 217640235, 1880493927, -1671735529, 1137613142, 2072545208, -414851757, -1785997391, -364718164, 450315208, -993471993, 768175939, -1566579292, 85961510, -1827000830, -1893503205, 869202084, 713571555, 680257288, 1524440291, 1741022434, 561415328, 1990319608, 1142451744, 39401847, 1221297801, -2124038766, 1215377498, -2068455826, 560063055, 383922313, 7329552, -1417241590, 1973186515, 358937975, 1808732034, 894888594, -1620703934, -1409454021, -224706429, 631015427, -701827114, -1980442971, -1243431585, 1865483925, -1340041763, 259984294, -1443453841, -885229413, 973067512, 780961235, -282514052, -1110338800, -722213025, 1714985605, -1287879595, 1509400751, 324286798, 1011968175, 1774625427, -335835050, 1241953488, -485251005, -2023480468, -1498664236, -1676758135, -2078759270, 368391173, 1770332091, 602035732, -1157125163, -726848951, -296396612, -418101410, 1516209091, -433026570, 2065899179, 286245383, -1428168800, 310716072, -563791242, -1325785953, 1826452534, -23905747, 1034013849, -1085065618, 1611085765, -60799609, 1082236453, 561831452, -1827984069, -277941810, -2097393299, 1609593516, -1947366285, 2039786925, -2039232768, 986451997, 2119304777, 49748214, -1530450382, -588012225, -142349556, 1234615466, -1482467714, 728929313, 438851997, -424861037, -1835013005, -674124377, -1634348548, 1081331853, 2111035427, 143997944, -1158230701, 4815417, 2122369877, -77009634, 282329472, 2124624001, 1395262123, -602351149, 1496495731, -522090375, -1089014497, 1060099030, -514142834, 624755360, 101709947, -259648574, -1721466978, -1470128315, 1344990842, -2138737258, 101466176, 1692425055, -1157926775, 592741389, 1813083585, -769169250, 1770253928, 1208684737, -702112980, 1001273019, 1705993099, 1407346099, -2142523547, -1355363485, -267899641, 449328343, -987691219, 438101969, 572223309, 379113218, 1466899667, -623010689, 2125548615, -145443483, 631502783, 1728343290, 1277749965, 1997442958, -1429886186, -537022197, 763891225, -1238739363, -821719020, 940172257, 114964281, 2090254185, -966856290, 1594918376, -1912990965, 1325705675, 1909184548, 837435170, -590257590, 1748272543, 65934393, 2073600222, 170572472, -1901011521, 2133543824, -1551997487, 1825478098, -941111977, 2081346119, 1276024247, -1737235139, 1172151357, 1861822828, 2017860579, 2079359170, -712881259, 353483674, 1081877284, -310138121, -1387900910, 1509477224, 321767828, -334162604, -1426416668, 122601289, 900426562, -1974038173, -187934215, 1716122553, 536633084, 653559614, -106459236, 612788932, -426096009, -407044580, -231495552, -20598604, -1049988598, 1707164387, -907341708, 1018148334, 420273830, -717817139, 746522674, -1091234728, -769304365, -1783917863, -1773360712, 1421244394, -1489877988, -1400774353, 704671809, -523850319, 107160908, 2024605373, -799692707, -2092464355, -948361722, -1132761744, 429369122, -76789764, -1551036156, -1351725409, -11045966, -1316255914, 1121595316, 1364255025, 1812124631, -1134809617, -1230048918, -1823006270, 103013418, -1985924618, 1276352832, 1604221273, -237209206, -1822616069, -1899068745, 1297703890, -240045011, 810578223, -1422419765, -1418704599, 1034032605, 2085440174, 607645733, 716362365, 1235513555, -1211579413, -261155896, 2022908495, -146539076, 1167671484, -211945140, -268072629, 40741212, -317939085, 728869511, 1342184697, -522128634, -716993901, -885638830, -1889540956, -518758183, 194076888, -263047735, -53295197, -2039369321, -1402107402, -1232069700, -860885703, 667080371, 2003791013, -1792537425, 593890515, -302918528, -371191726, 915728277, 1775934623, -1884658077, 1983888460, 298800478, 1016157169, -1717781878, -1076292572, 1732073196, 542964773, -773239025, 1070547456, 1719362726, -1490080193, -1399780184, -58541011, -1591258, -1250990694, -443129975, 1822357515, -1774941626, -1423917059, -1324183435, 1247654078, -785941226, 208759350, 1371670412, 1903510098, 2128083745, 435649658, 1127890999, -1861063799, -188564302, 1199643492, 1891452416, -217657738, -67141750, -1266789415, 2131626424, 2098938511, 1874390421, -1698831352, 1922731129, 1143118810, -2026197630, 2086052126, 842500141, 287962959, 850955114, 2012362088, -817258418, -1072214227, 978057684, 992062798, -2041866817, -1611489850, 1663409654, 112766564, -1689406122, 1616786320, 556057860, -1680102493, 867719167, 453575899, -191805706, 1712061526, -744377824, -615870979, -1980362202, 1649307499, -613527529, -514007552, -354868527, 740361284, 1191787483, 1421727561, 1066283904, -452434665, 2020141000, -1987374530, 412400833, -621803967, 20900810, 559102704, -443346658, -768206607, 1402289809, -1479041896, 1359182666, 84692384, 1919671125, 1665432592, -1427511811, 1351138729, 714150331, 1584608034, 1063897075, -470363603, 1537682572, 760337828, 270984358, -1339485809, 467876006, 1515737109, -2141726672, 1046916347, 1259950801, -835983188, -2073384503, -697440699, 1343223043, -1288734811, 27645887, -1066885181, 2063044057, -56607701, 319902811, 960858771, -423030408, -812161836, -1112301146, 132484238, 1783289397, -2018957458, 450584409, 1012115988, -2101400823, 1667035362, 1107203875, -1865977929, -723361763, -1343871789, 1135679266, -1675492453, -140706303, 1364740541, -1551211173, -2009393394, 2000971427, -344052593, 462623413, 143090848, -1640955654, 1157518396, 659813664, -165571783, -761091080, 1439584252, -52830785, -1885945630, 1884406245, -555522218, 1323853722, 930747959, 137706091, 555548831, -1337759477, -1009674506, -1977870785, 1180081172, -687421630, 194151065, 1311924712, -866937125, -137781558, -698706859, -1895205467, -1848499551, 1896490516, -6509636, 1269553250, 186532024, -955818569, 1845517066, -400727025, 1078611153, 863814973, -1229137047, 1718754324, -216510561, 1988750453, 29465919, 1428890551, -62281515, -937668540, -1508270436, -927907488, -505451885, 1033857489, -389957828, -2065486196, -352295525, -2105963968, 1299134698, 816779483, 156423679, -1354381381, 1887465750, -2105822745, 642600242, 1123616314, 188710252, -1703216607, 1459661161, -1941560289, 601336479, 1863482085, -857985266, 794305967, -1660447453, 226783646, 241199673, 583367867, 849630317, 1914170489, 565711020, -1488638620, 609086194, 1720536967, -1694564352, 692492707, -1506800749, 730802235, -157471351, 242744029, -164780657, 554729192, 826406260, 2052603794, 1509424364, 880799424, -742089480, -1122708577, 1850636033, 1672099719, 1908731732, 1738334895, -2040611202, 1682998097, 1398609974, -1324949149, -975919403, -1450888087, 1833224637, -619514125, -990582005, 1412067944, 886169183, -391523199, 607372595, -1262130460, -1519841199, -1773159746, -1708684329, 1508540061, -445129927, -861216001, 449901651, 1557438209, -1188736704, -630147206, -679376511, 1198115538, -382787307, 697875997, -22939436, 239787497, 500731101, 195546534, 1392914720, -187209041, 455847608, -2049957759, 766204445, 1368826958, -2042625013, -180992444, -713812831, -114800611, -607409323, 162793232, 2138008530, -1531267188, 868044052, -1630059848, 1621859247, -1597211643, -1129166747, -1199701638, 1770783044, 36166445, 1439401965, -994866018, -960772827, 2001685784, 441293150, 408861924, 905891633, 1537313206, 400637893, 61265814, 1571963795, 838433145, 2065601099, 778646834, 316955585, -2087195141, -1175880744, -1556081321, 1057881099, 261925029, 1208410025, -1666750702, -1564870443, -1780046839, -921180273, 1249930686, 22741986, 1111587522, 1806539596, -2004101869, -1217186294, 1838807150, 1025186692, 1739799205, -970775152, 1248070355, -507661275, 1255915477, 227039459, -1806354804, -1933273622, -1702447540, 998405321, 1478470466, -1376315847, 30712562, -2027352328, -1528293401, -1983304959, 504320567, 1291680060, -1444744047, -1127727805, 1549237293, 1204875828, -290551371, 1890491263, -60192594, -338589164, 520299155, -1570639410, 1365342605, 717971876, 2100041137, 950014485, 2111827591, -1614588413, 1565446784, -711540009, -612602607, -1878381653, 759406734, -1354242425, 1036377793, 283764256, -147639272, -280351513, -314754805, -993828539, 998353033, -1202064568, -1057618001, -395391049, 1549721165, -598972723, -982907535, 1557165381, 1891640427, 654353458, 1775642645, 935383528, -1688413182, -419838142, -1817002350, 1500587707, 439484714, -671255505, -1446765092, 1379929086, 284924340, 322973021, 517663367, 1269409562, 1635098653, -456602725, 216521789, -390880857, 22702718, -141949792],numpy.int32)
        ca(self._r.i32_2, [-461364931, -881174363, 1190512124, -652344200, -1904465790, 654215830, -8237446, 1554134258, -1171405181, -2097329372, -1168547037, 4964041, -162499187, -1566779923, 396658647, 1372847452, 1952977117, -2055030887, 1369558008, 1159869637, -151488968, -1230916956, -1662654082, -692556634, -2108882739, 1919783279, 86726599, -479175753, 368307099, 263085896, -1297854452, -475865862, -1052798892, -195216089, -1808717864, 1435851230, 213845163, -2014435943, 1958739019, 1950538379, 195043354, -2094251280, -552928187, 212026163, 1882789473, -1701156512, 700729029, 617009319, -51379635, 1437981860, 143582562, 1759700160, -1043283958, 790685144, 1053455552, 888961142, 1884764193, -574487120, 205387093, 1706716858, -1564706331, -1119162850, -320357115, -216356729, 1133115157, -1585595150, 1163420546, 2095530513, 959051309, 1266503031, -1940662617, -1207768369, 2071048923, -247500208, 729695364, 1732441574, 919515230, -1307758899, -1362232635, -985845056, 1183002178, -967666429, 61839483, -797969544, 1019207261, -2080745651, -1493399698, 448039065, -1006260032, 547484182, -433873666, -145482008, 1266128764, -374269118, -148627528, -481205875, 28560825, 1620567461, 160877005, -152736921, 566726869, 1690610724, 1551218429, 129384906, 1756514951, -1619123979, -1635458102, 461420293, -1025697720, 1074881682, -1342853402, -2024581138, -1021476707, -979756855, -2061951658, 495595484, 1072057242, -1075816975, 634930689, 1462757877, -355459145, 113806554, -1586994022, -1759236007, 1642313755, 1844726616, 263774839, 865591847, 1137711548, 568540382, 1697402204, 1287333602, -18557107, -543522023, -747044673, -894978937, -1633590316, 1469569043, -1916659051, -245350462, 558791729, -1069756095, -1671183103, -675709621, -1496240619, 1002596182, -1049603233, 1067628357, -320684962, -1756926613, -1978637534, 2115134917, 293851213, 188870457, -2033713174, 316694162, -1680926305, 1578104820, 2019431451, 1672278268, 518272185, -366138444, 1261822504, 1003789835, -595796762, -1764183978, -1066900678, 1415600408, -173332206, 341584118, 1836086928, -77555270, -1989963843, 428500682, -489840295, -1096671034, -1915424250, -1746745758, 473428620, 1155878488, 1534484342, 1866809635, 2125417205, -356683367, -724519561, 476765866, -509611460, 1067343485, -1663160103, -1973204454, 1891962125, -1486851183, 539703058, -78175960, -1038870474, 585234261, -1015599511, -1860840029, -1939494917, 2120890829, -1396051426, 442584714, -559475888, 1852553473, 1370937853, -189979498, -1942748392, 575014321, -206759426, -31154557, -2070305927, -1863241823, 976830155, 405210820, -1810403626, 1246769487, -1690543149, 1313271912, -351123144, -169833423, 329135592, 1471013659, 1018659812, -1227714342, -191860948, -1335651686, 883360682, 836140176, 533570354, -306737045, 503171813, 1574245195, 486740175, 2103577114, 1369514515, 631086314, -1519000748, -1651625120, 2072505877, 343400009, 1919137338, 1103988337, 2071554186, 150773570, 2097705645, -130202734, 327475069, -884235865, 52111222, -1080547500, 682409781, 1559839293, -1958998234, -668500619, 1652828958, 1898194722, 1411170984, 2027809940, 2057915321, 624976316, -1590230095, -39277437, -399063086, -199887533, 1695889089, -179411470, -814891514, 441001215, 228328910, 1969824685, 1673102538, -939256124, -2021849575, 1292458519, 1963232860, -701199322, 1898059105, -2045458245, -896773856, -465102206, -1132267068, 1715928377, -1576771507, -76241412, 1187144803, -1067322651, 570283207, 1328683328, 1679817753, 1351131251, 218112167, 1288274663, 1769551475, -1459879021, 907399627, -129113618, -816814174, -281922806, 1308242407, 959061391, -643658909, -1586885260, -731576338, 872407494, -1435528398, -978470065, 561011867, 2094464646, -1961457104, -370593344, 173444003, -1787659154, 1403917210, 1314481998, -2064760703, 627159779, -1209896425, 950681678, -1599356229, 1797678336, 1407713282, -1860763990, 1818135625, -797982794, 1766490463, 146950743, -573489171, 541336457, -786031692, -823206893, 472702619, 301835709, 903962039, 334036788, 1308489144, 1982571588, -1297489003, 1027291239, -1050223998, 1301065587, -131811840, 840706119, 151612697, -1514662009, 2045477247, -78244632, 1428738052, 999845946, 632205998, -2084777797, -1263080892, -1527740973, -1052672864, -1148385231, 2118437588, 64244951, 610247700, -192213951, -1677840790, 695619117, 194487568, -1064818224, 567953693, -556351633, -358984117, -543035561, 1299534234, -1814192015, -1987974286, -251589327, -1550216573, 1039391427, -648231381, 209808513, -1809205905, 425289643, -1478441699, -499830484, 895438284, 1388891777, -141187536, -1921173432, -2109700894, -629643543, -1992180854, 1262181466, -1000112113, 1891981448, -511356474, 678112000, 231308715, -845426086, 2065931343, -690231821, -2065441467, -497137258, -288817447, -272642500, -1778307241, -206926623, -1058833162, 1207480823, -577760388, 967667904, -747757357, 1515713516, 1901169583, -43384102, -1869097267, 698722931, 1723948263, 895747277, -963077288, 2007160291, -1139652897, -1941673179, 1182316407, -1504345279, -69517474, -1337091986, 1144745436, -295343637, -368530206, 423117467, -1160707313, 606107242, 973575490, 782358427, 1225701496, 1354180679, -1819084457, 210496900, -1607248517, -100403486, 357128435, -1211000784, -1699635523, -1995757335, -2041727997, 1639346630, -1140917407, -1428441321, 1391552530, 950439976, 1536850187, 1755763383, 349315024, -1716747422, 1788059719, -956787148, 435093165, -519717781, -1185043774, 1326150846, 666841562, 977518902, -1878116663, -1052216208, -159814671, 545626237, -1161390691, 172913262, -1143147285, -711220581, -2073758388, 1347605160, -274461216, -1138600943, 1812589913, 1321776791, -654185814, -514865093, 342576025, -1227661029, 2027182643, 499090278, -1057042386, -1200362684, 1633068952, 1127338030, 66338457, 1655244407, 1091076049, 1868857534, 1902975017, 427968982, -689633450, 1869590905, 828919724, 374348665, 291496172, 369492724, -1956000730, 149774736, -283502913, 542857976, 1810830261, 1711344293, -1158072113, -1788295198, -314318981, -1029216204, 1180472328, -769273193, -1884508206, -1558495607, 19086583, 2059341589, -1133755497, -2103950715, -353373479, -330597102, 146329926, 1139012057, -1595155154, 92242787, 1758776536, -2142059846, -1016391823, 572794885, -1164070685, 936895954, -530252487, -852015578, -1387262267, -610552571, 993685216, -2060482368, -54855358, -1368415548, 1727532083, -1998919251, 1004938093, -193604754, 402127614, 15533913, -822374248, 914869992, -398825428, -1951818825, 1024562104, -1513050369, -1086194365, -1602294388, 506250848, -450950473, -1107350963, 724811630, 1667267553, -1296578611, 1797492484, 1593191271, -797438732, -1327763127, 1815794923, 968830944, -1597687229, 453031735, -311267208, -1363949093, -680526092, 2111164100, 1874373703, -737231277, -1941054345, -1943683241, 299275156, -777764717, -1580845667, -1590831315, -706883071, 1006664100, -455650726, 405499155, -1557738572, 1434435376, -476662082, -390599384, -1023097080, -462139722, 1416922513, -1243778374, 1721356353, 2052478481, 1576465185, -1753145409, -1866886190, -709091910, 1188370346, -47903041, 833750418, -714362080, -1356224125, -1264932342, -2019192812, -1865286029, -872940604, -1103730145, 960420100, -1042876502, -1376735106, 652488617, 265536834, -727122450, -1304252301, 1452309463, -345462904, -1385578434, 1005791488, -1952157450, 1535232809, 1539175065, 1764693654, 370125766, -1202518768, -1045824063, -1277351352, -209760871, 745809202, -969253860, -263968717, -1987049520, -994220477, 1014895379, 767424874, -1455749768, -1031331847, 102844430, -1853475234, 1375464119, -36893052, 738438714, -2023227099, -766955665, 917641510, 2098209786, -1217824087, 1658975849, 519874226, -253260859, -1162718483, 1786747123, -1141951794, -2107503630, 454499128, -1967565552, -1023321135, -1996284503, -752431392, 472701630, -1632851902, 410108660, -1046454863, 1967316776, 855860213, -1312902400, 2040315518, -1117439624, 493239897, -1998091182, -2034474271, -1097999735, 1318127173, 606300235, 1842233668, 575662433, -2004034017, -453132858, 575442626, 312602259, -2052800210, 1864640938, -1558226144, 1723181891, 1563560258, 1335087794, 1484455993, 1617896015, -1725417335, 1319720221, -1761963217, -699139792, -1289651408, -1107156983, 1743906484, -4909723, -1308860494, -1458950358, -1346838156, 770842123, -2015270071, -24732450, 1317412484, 713576473, -367369916, 1304052776, 249082034, -1501300599, 440635569, -1918514505, 1703744454, 1979510875, -1459719502, 2080733946, 1591601168, -1279512428, 1050916259, 506633589, 985141457, -1785288990, -264273336, -929708322, -719186799, 821741784, -672362448, 552181928, -802373915, -390543422, -343050866, -1958288614, 898584575, -2009826787, 695541207, -490634204, 1677702760, -881113644, 949838036, -1754707531, 1625802700, -2116565724, 1986923158, 755539119, -1478875610, 266787239, 1794560040, 1005034935, 1558408357, 763790383, 677517420, 2072139195, -235728628, 1725705385, -1582053707, 1113461586, 1674642759, -1414719663, -608468252, -1873260761, -1401304493, -1029303396, 1873534265, 912963743, 645715337, 1132031991, 487696799, 1110621999, 1383752223, 1018103642, 536280867, 1764666589, 1624759145, -707782673, 1407012132, 1887436609, 568473975, -758524638, 1093808445, 330404853, 240981075, -250484760, 498674002, -1126343191, -1070540555, -17257403, -1302522037, -1500566183, -706742387, 1731391627, -121892623, 1944180, 697150366, 1175869801, -1081726694, -772936078, 300113930, -1519743318, 1011619084, 966435032, -271530967, 1478437384, -2000885569, -1625488897, -30409891, -577640443, -491669659, 1721990364, 464531779, -1035520457, 1234811766, 58268492, 761680308, 338102126, -1281454585, 1554633851, -2008859178, 55616722, -2039496630, -902950403, 673529549, 1020509295, 1518665847, -478044459, -296723364, -2075845731, 1809506854, -99500436, 883142933, 289332182, 738556337, 1501633470, 2058318873, -346819242])
        self._r.u32_1 = 1550099195
        if self._r.u32_1 != 547919123:
            raise Exception()
        self._r.u32_2 = numpy.array([237099665, 1725693514, 3671290215, 2838122575, 2174235839, 1926762547, 837710207, 2675306390, 3296759548, 3236712776, 1185582523, 3424554628, 2120088772, 3672727628, 1229489468, 299615394, 2391828662, 2161918065, 3215046430, 4090719326, 4046969338, 2837195073, 1814520605, 3281278603, 2366669618, 889646058, 2889818005, 582950935, 1660657214, 3304485267, 3017091402, 4182786222, 381383578, 468232037, 4264726246, 548129943, 228487325, 1626908942, 3843628003, 340032714, 896193553, 1589965383, 421647904, 1025804481, 37483739, 314532432, 2655347560, 117434633, 503953090, 3976906518, 1323855325, 538108471, 4161859424, 1912643799, 1352908924, 3415941572, 2123957567, 2125372546, 3660361032, 2093953170, 844556942, 350952258, 3712309630, 1671728833, 1515702177, 674196370, 1804290265, 2369213421, 659681625, 3007121556, 3629421992, 2355746396, 1887771, 1763854265, 3669589284, 3060951582, 2289752966, 2753656458, 453476287, 3858397040, 1755557022, 1056528532, 1074824037, 3392115327, 959387159, 4047339053, 4055444899, 2701521116, 3269246259, 1658313101, 1191016218, 2976266754, 4058115909, 3148745595, 2255966436, 1286833652, 3846605743, 332980236, 2987111809, 2863137443, 3589002629, 3634508729, 3050304267, 426166523, 38644952, 4120741158, 3779249472, 2247004208, 3887627978, 771737466, 327488668, 2413511241, 3742352323, 1800531129, 3093397506, 119855689, 1044449337, 1621589532, 2435672368, 2249934961, 2486385468, 2733265378, 2055466545, 3463839050, 1741434858, 1937180913, 53147295, 380685724, 2147133772, 3377145922, 1696161493, 986108230, 552797714, 1030805428, 3633258771, 724378483, 1453096552, 3633745301, 722493301, 3218821892, 3672842476, 3232339885, 2194639207, 3626117658, 160139022, 1220950174, 1499215195, 2900860877, 1105932921, 2513047638, 2975567394, 2688547895, 1701949245, 494851022, 3099438803, 2302405511, 3002890773, 3694596195, 1818301109, 2241585621, 3375937719, 2173718080, 3174769392, 2332849203, 1120354034, 3688107993, 3910547603, 475511452, 165704715, 2543590060, 4279301981, 308235882, 1816022030, 2611287885, 2638354900, 1603444131, 2625463614, 2748122332, 2695819720, 3508062749, 4213882116, 1456900955, 2527945808, 1021825166, 2050461441, 2014465404, 1165369542, 1735932899, 3460204932, 1482933068, 1853558960, 3796877889, 2819245867, 1495722807, 286085468, 1232127264, 1369041740, 1203310608, 4013214417, 3662137316, 3906425458, 1886277730, 3592347464, 4124894145, 1520615672, 2057935984, 2780423261, 3807868959, 1096708615, 1133308613, 2081283278, 3031731081, 777297905, 728628197, 1045968931, 2798986608, 1441163940, 425803298, 3425923673, 3174138272, 225290447, 2789342514, 1500710940, 2214009944, 2611052505, 1511169866, 3468976229, 887023337, 3301621653, 348051316, 3413528372, 688050819, 3270149113, 2721404891, 2790531383, 1307526009, 24196953, 3323021735, 1883300819, 827261292, 1024782357, 4200877565, 961985674, 166365221, 3011947146, 3773678739, 3122249899, 4236359826, 3567170538, 164427914, 3384429677, 3901604544, 3178054797, 1736839253, 2964545385, 891428101, 1944593339, 1989423560, 1361523913, 3168022842, 3512787479, 1890231449, 1593427930, 4149710413, 206469070, 1896704648, 1231454209, 4068940405, 3271655038, 2008435184, 2914967896, 2357818161, 1859278865, 3410094777, 1298228364, 222292372, 1055108733, 4040689906, 2210549194, 1948747, 2506100330, 962472296, 1968083925, 113875684, 1936131419, 1016307414, 1060859451, 1739828182, 3346648079, 1164081840, 2485888280, 3476085289, 585721471, 390929102, 517669802, 2653223889, 1174053498, 1569525180, 3310507972, 1002962122, 2262804195, 3220775546, 3182459697, 2156503148, 4131684371, 2813459977, 1117022498, 1997829290, 2683851565, 107074302, 1419327824, 3915955155, 3780878619, 610899511, 1901058671, 4050293718, 2053491262, 1391571066, 1177627511, 743398950, 3803305715, 194123827, 3621325995, 472267748, 3375152783, 2897163902, 3462255512, 4250233830, 3994919468, 2831376517, 246739001, 2563541164, 2158887230, 3637942716, 2966210109, 47815115, 521677298, 645694605, 3228944885, 737962495, 826169136, 3548976344, 4043510480, 495863083, 777697689, 805624668, 1263172222, 3510345575, 1056092728, 2969537722, 747239264, 3369168528, 1344872701, 3335255317, 4214479629, 3890217901, 212326383, 626667851, 4084223303, 2815290146, 3385778156, 1708926854, 295550151, 494270470, 3067952778, 1533064310, 2934900292, 1705387163, 1307922285, 2193031516, 2433387564, 439649015, 2639844157, 3899988054, 3512645808, 4082111285, 39460185, 2109679546, 2807623639, 872015072, 980218181, 3396910791, 3668142418, 1001890199, 3235923562, 3566499716, 363410876, 2673237222, 573356352, 1636136151, 2224553312, 3704628010, 1623877736, 2563570732, 1232767726, 2971775467, 4216718036, 3488020769, 257411122, 1168087703, 818565641, 900860168, 1947568647, 164818961, 3931611634, 3720231207, 2690894061, 1424779930, 90538671, 131364160, 616530415, 743044912, 129491467, 4041759658, 3433286148, 4169430938, 2922959631, 3821215730, 3097046213, 3611435200, 2326824436, 184884915, 2069988071, 3914342196, 106319212, 1325869172, 3906567559, 1758481342, 1277175140, 2754342337, 1294820705, 791996734, 41241012, 3345622322, 3718866993, 1255338839, 1391956142, 3839078475, 3457508262, 551513656, 1004850662, 3795985935, 298265118, 3742037297, 3355517467, 3601723593, 3585988041, 3063759488, 3171470181, 4259702765, 3239000394, 2708065681, 4092601030, 346908933, 849213263, 2851377667, 1796454246, 2735073999, 2777745491, 2294240001, 2121652435, 2706284022, 585848169, 1936702478, 2371114722, 1541583037, 116304242, 3676364969, 3879455349, 3833621771, 3701696564, 2780518089, 1479844512, 1789233460, 2165430981, 3709637684, 1215700310, 3383152932, 2134182167, 3267525810, 4142614062, 1913035686, 299460925, 2677124325, 2261142050, 2007429043, 515722793, 25703755, 3410497288, 1661381183, 1667524384, 530887788, 3517835794, 159256235, 3805603779, 2368397, 2999883232, 39771046, 49747199, 3734347231, 185140859, 2259304947, 3389847559, 3758478898, 1438981583, 1923428196, 4294696986, 1917080172, 3599354053, 813437110],numpy.uint32)
        ca(self._r.u32_2, [4251946440, 3334867394, 1627635129, 2588419147, 4174027116, 3897125158, 80443814, 1389733726, 4117149812, 12542280, 1256007817, 1703348194, 4237384057, 1454512978, 2775061970, 3298540861, 3715621276, 2362002640, 3636980763, 3430743390, 1830381203, 1507092396, 4142499824, 4213673901, 1183960426, 1874370435, 4181283334, 2200901254, 3332790298, 3423644529, 2387935836, 952382132, 3924524172, 3719680299, 853249098, 4083610173, 2636543308, 657361882, 1525744446, 376298547, 2451684942, 3240929540, 2310416762, 730671377, 2937427586, 3563592349, 2472196520, 2147357762, 914655107, 1758244054, 3876886042, 12351564, 1679162795, 1489623257, 2455794558, 2538372341, 2057637059, 3508778762, 567682489, 283434754, 3167627543, 1915532592, 1232942381, 2754609078, 4150346060, 1663219004, 1231896519, 2755959635, 183820585, 1055352125, 2147188623, 1645909010, 1893712235, 1485051038, 870164520, 1966826561, 48501444, 2556720793, 3128066451, 790988700, 865202135, 4263049716, 2090861867, 1748977625, 2699841095, 113797990, 2481195137, 2574284167, 834141103, 476065944, 1480757910, 315080683, 350708905, 338916974, 709575589, 3077697353, 1231129412, 746021816, 2332229547, 1946675456, 583346238, 3135681244, 1842291655, 231618544, 104978643, 4086067348, 3174792638, 1543369889, 1101673653, 3023672083, 3205010661, 1536466390, 966572661, 3883854770, 3427219648, 2247096744, 4079126348, 776176295, 2599372279, 1888032134, 360725842, 3052443662, 865793013, 3084628677, 516162558, 1020425629, 2915535067, 4215116317, 2977464272, 1660722837, 3507058298, 864890045, 249379031, 3973345746, 2629825645, 771115239, 3526813236, 3106614042, 203525488, 2971666751, 2845337507, 1637317812, 1743782319, 3991795965, 3057486763, 2839184028, 2831552101, 2836007599, 14115933, 2147447119, 3904004068, 3346997713, 1322155226, 1049159718, 2520132354, 2765453431, 4205328777, 4063219623, 2238279021, 1619016803, 415896490, 3591765870, 3318597287, 1557289292, 2845067684, 89482247, 2114516871, 3464828768, 1114311788, 4215401081, 3458358731, 2736518275, 380431203, 3435888629, 4249714953, 1764633576, 1915821483, 1597234883, 111251916, 274107180, 2935452271, 4072034355, 357724805, 1550422867, 1378849275, 3264188640, 3028697235, 2805673388, 656257910, 1454961285, 188865944, 1924561757, 3184772136, 129725152, 1587697966, 106462817, 1587951867, 3192757556, 2829152265, 3270745049, 435873692, 3749929242, 2062096658, 4149869860, 2418404390, 3646774382, 343128996, 2496743364, 734565947, 3826051517, 2828517029, 962692901, 730853036, 1082602175, 298823790, 3231844899, 526460170, 2579457360, 1480606553, 1842946907, 2622701868, 3895551897, 2026981125, 3153668454, 3704749050, 1185971623, 2504477989, 1870109318, 1518600621, 14687749, 3846239097, 2613355571, 4011868731, 4273118207, 539188665, 2099254272, 1043640546, 2517454961, 4147146631, 3753370580, 3811721724, 989962603, 2211483632, 1480428764, 1954557704, 1112461942, 1569266181, 1678583802, 1646459706, 316406457, 3242999591, 3888012390, 2402113654, 746240298, 3662473135, 1260156363, 1203238376, 3061859356, 2032152659, 966717679, 2534194659, 3388402620, 3223059378, 3877902454, 2566178070, 4108564664, 2578614366, 2924743698, 3967226306, 1346866215, 4129141259, 2159606690, 237374413, 2311773278, 2936435723, 1669343609, 3835118141, 2474006294, 2312776854, 3991958455, 66050323, 2021998927, 3191454066, 2189188580, 2142686591, 262029985, 1334540897, 877178233, 322292574, 583880104, 994626866, 2643853709, 2746736170, 1819097952, 3500683162, 2717819610, 1979841756, 4158317627, 3768907483, 4144867490, 2428342768, 407254584, 3876466370, 2906963449, 2747730439, 2807429483, 390805623, 1347724002, 3708124771, 1996426487, 209852741, 3539291907, 1973958470, 930781564, 3333035683, 555854849, 540149787, 3214341438, 1165683130, 284698251, 3229514555, 1944044250, 676799831, 3415601775, 686883721, 2475380401, 2417075124, 1731220395, 2692854334, 2090593377, 2377595670, 3031508806, 24480902, 3556421449, 1940400454, 3751271557, 585927728, 2399018121, 1897248871, 4110307692, 1294121928, 2976700231, 2519149970, 2393660481, 1452332020, 1320620207, 2261085851, 2445477360, 3141380218, 1044718590, 50521930, 112491419, 4149332237, 1091423792, 1469962572, 3907732209, 3328879500, 4063642960, 3006889620, 425720040, 2842213341, 2094386140, 3171166176, 757382335, 2515418722, 2466505128, 4181749776, 3386253778, 1241141486, 3110299582, 599382492, 3361936057, 2904521896, 3463235864, 1686895148, 4096837571, 2649784396, 102145162, 4034413105, 1309891308, 1727749117, 4111125789, 3485689078, 1298526747, 3208723720, 1387080573, 3497204630, 2701756222, 866112144, 3332181807, 2824696606, 4019789661, 1393196838, 477838543, 3838343203, 2399752805, 1676970714, 2163423971, 3918831727, 2082667742, 687058482, 4132123776, 2944329588, 830337633, 3305684867, 1115400173, 1409924819, 4213431551, 101974285, 721035281, 418956469, 3537419424, 3058980494, 3735712173, 31898322, 812527641, 1412975070, 214035881, 3370497326, 275023508, 2188096928, 2698269714, 2338536560, 2217867267, 780724394, 168999967, 4028242661, 2057116599, 248770288, 142100118, 558526929, 367796080, 1613088719, 111252491, 569035372, 2444968023, 4163888313, 3008206018, 655301551, 1102089047, 2157711351, 1189565715, 1048858627, 3463105328, 1659606364, 2839652561, 311401265, 297227948, 2049718821, 1287086069, 2816817582, 753298510, 79123064, 2058422267, 1988231070, 1697021200, 3755875481, 2000787653, 372680790, 770642272, 3557979977, 3242763045, 3424268849, 2545039983, 3403101537, 804431778, 3022051943, 1799982329, 835187866, 1307679719, 795446639, 2865087004, 2503099400, 1097854687, 412079412, 2918593238, 4204336449, 3272876881, 3701287131, 215671154, 2729194459, 3828900376, 407889473, 2386020434, 1672155598, 1588439879, 2355888880, 2451706408, 2223568426, 4230924842, 1121564168, 3971399371, 2302823247, 1838239260, 4017581704, 197226193, 1773201901, 22730505, 599013585, 2360399780, 3459055993, 2359729316, 2534122212, 3338162386, 681551474, 804682591, 3684776026, 2611917837, 518924291, 3527933723, 2831363989, 2092857661, 3011292035, 2036768662, 1165948954, 3915111934, 3715091842, 3486642823, 2169348932, 2210412086, 2082504433, 218262071, 2666551070, 3844955859, 1885787522, 50919684, 30300958, 3237830009, 1004399278, 1420324202, 2995067867, 3343455201, 1341482320, 2707911315, 2322962795, 104691279, 433113543, 1673935915, 237192280, 3866873407, 3719846074, 504926120, 1585743054, 710382710, 2276436306, 2976938826, 1322735386, 1856969923, 311925360, 1497000075, 2852252785, 207694370, 3237126868, 126779936, 696212993, 3860732454, 2811018481, 3182218492, 2694262689, 954054185, 1145279765, 1827792779, 647535690, 2378645894, 1603060963, 1501639457, 967601596, 3979534574, 2129057469, 1503074666, 3455573355, 1277747107, 2364423785, 718418781, 2029920441, 3230465514, 3292224990, 796319542, 4143628522, 2357283776, 3321794845, 2371483975, 1136784117, 2757314460, 132067372, 294498845, 2989608361, 1147501898, 848670725, 3702484846, 3398317762, 274118355, 3486956662, 2414417547, 4165976855, 3707418163, 3614978249, 793009306, 4227283826, 2072607460, 2291123052, 1319566667, 3736885972, 1075733989, 2822123350, 883768237, 165340447, 2283477403, 3854687889, 2702364501, 261781101, 4253180939, 1904200988, 3670999235, 2081253795, 1013385256, 3393606543, 3915738401, 3677841368, 2222722431, 3582521284, 2184635962, 1379820344, 4132361812, 3076369748, 3111110095, 1060089765, 3951504597, 276119608, 4292130693, 1208342406, 2964718231, 1156835032, 1503506724, 17689181, 1253790050, 2052448727, 3951262449, 1045066741, 1212371757, 3864687390, 2781636814, 4164334487, 1434750495, 1015217609, 492107542, 4106176432, 4258301116, 52857279, 3601017578, 553436516, 1286022350, 2970181802, 1531473162, 615711544, 2770114226, 3807138554, 1254115612, 405024141, 2248962327, 3661682788, 3457720992, 2391719239, 3782958744, 3184983441, 1120404266, 1505151243, 2382314268, 4164517871, 782247452, 923774834, 3508260701, 2537984828, 2116287910, 3255992169, 2640296699, 614769200, 767427138, 3456406779, 1809700841, 2437468993, 642938299, 3155191374, 4074085350, 2642920857, 3189984175, 3169851773, 4086000673, 2490375684, 3948311217, 3105674217, 1698869289, 1311043867, 193634359, 3011562913, 4136987101, 3694637471, 3746665664, 984905715, 1842085529, 2014624560, 1012559384, 381626366, 3316965712, 3951018504, 1396133012, 2477956684, 3892489603, 2447107565, 1585934707, 2614794953, 4048636321, 697301886, 2382428822, 2964257243, 506994596, 1901393962, 3958702238, 930275666, 3970480891, 2137671677, 911161575, 3800494155, 278586712, 1193762952, 154795879, 3301269187, 1668521332, 444082092, 1753908500, 1687735396, 3236812133, 2861130228, 179908202, 1539423798, 1280312575, 1354412234, 890265444, 3698680851, 653081540, 3681719879, 838283359, 969405299, 1918696509, 651424255, 1081467498, 1369194422, 969636592, 1353343686, 1151142771, 622249210, 2324152022, 3419137792, 2402401643, 417315756, 2283635979, 2730135008, 945357607, 1421847419, 546033882, 3198842674, 3343416782, 1103542692, 4192435052, 2680753787, 1928123125, 1829821471, 3877076359, 2319958157, 1817991563, 3019027601, 3350099005, 122241996, 2220681659, 1867304134, 3903645175, 3926484316, 561272258, 2924762331, 1521681554, 4276247138, 4264605013, 3489960755, 90524145, 3924010437, 2159859802, 3931840385, 1622645822, 3614003481, 4142324969, 2557247602, 4114169094, 2832266442, 1338437964, 4072229872, 3375287658, 2231757313, 4020609455, 2396693058, 2794056809, 1622056246, 3798643807, 3419424563, 1469037362, 3368075234, 2696057690, 4239384736, 2499585821, 488059987, 2262538463, 1978623658, 294535630, 3609960885, 432048986, 2518665415, 576966143, 1577963777, 3672258101, 1737846056, 1033455641, 3049863102, 414818580, 2310833967, 3876593023, 1159401619, 512103557, 3929750248, 104744865, 2294284829, 700010847, 3919829947, 472148418, 2495096228, 1476352517, 3466719922, 1423170701, 1835216137, 3804324362, 3156638174, 218238460, 2122719443, 1475392811, 4191547266, 1660363531, 1752963086, 814996542, 1775564261, 2768667643, 1691944624, 2673873848, 3717015687, 4274924722, 4267842589, 3218843587, 4086630122, 2525920765, 2642512022, 2581476770, 1587395043, 2479647167, 2075617909, 2220378822, 1164751823, 1254817289, 3012514369, 535781325, 1155411560, 3470618493, 3736078399, 727696447, 3668735551, 2540239292, 1287246718, 1034530277, 3398095154, 2277784043, 1007465081, 2592218771, 2307100491, 2280001478, 3781351274, 517873620, 16783814, 376212454, 1269327062, 2190745862])
        self._r.i64_1 = 8621740821050813024
        if self._r.i64_1 != -1357833931563696072:
            raise Exception()
        self._r.i64_2 = numpy.array([-1418708830105823852, -1357833931563696072, -8308127073437794904, 6203263204523798112, 7076661289157584762, -3645491092747259726, 2969229117250121621, -8403401867791621438, -5706351777107258259, 6979420050019736435, 1350986631885231652, -8626678967587677100, 8380704325304801386, 3423582193572197909, 8713973059069583959, -4562940403005824119, 9144900318464157853, -8717799056344934090, -8792498500921807539, -8345039878076898189, 5201358909840838683, -3398583150340629128, -5482869438456886726, 1644815108571813337, 7248497692538999361, -1178045319005427907, -7220532561583062381, -2882504460577706964, -3460274637164886125, 9053064536664375063, -8649931456492292885, 72282480921257410, 3058905063630457969, 8394362105178121659, 8263211448476405605, 8671703720724529690, 1117912130945798022, -7392161278301566795, 9070973456367872189, 5064083874137910433, -2216141782782730608, 6092600172408194906, -7328184273434559673, 7340896108422144895, 8041029351530593362, 3567042073657363684, 6634152186323571334, -939114094925119978, 3932918768588612631, 2223869457290740495, -1394521432769550065, -7708491921728269104, 2558409591077932690, 7323090212396920736, 4463226188281322565, -7684442752899854301, 3813932804031799733, -3061288894555894392, -8926314527654650550, -5483212417699975352, -5168152193234004511, -5252714907036148733, -8899682260331039592, -6945672564712903320, 1843836835216653982, 6265565553002088665, -9191803385169282118, 824381268893232707, -4195712559860724390, 3170122388521742267, 93238405484244323, -3808714570016938587, 7751370385159261162, -415651213975075366, -400640794129234242, -3632420176870277542, 2145224332581955327, 8408764257602201311, -5753925773175608181, 2442171188911603754, -718254550700219999, -5279112326876598860, 7731819115318618935, 7285784364016347384, 6648758251111712748, -4965048064766122366, 1799714525316551079, 5808264002475810898, -521447549589589148, 263148779791826658, -1256378489223837059, 3001523551318331984, -2133704098322946340, 9175731965505830169, -275510851941027307, -3450575930678805596, -4673869135690784872, -2779584507299050825, -6244919930307138446, 5663020090027727817, 3592337319079719462, -7699870730217589682, 3427192886285003578, -566635025493084181, 2780130284244381358, 3422425913941932991, -723427948584706426, -1731222455107826641, -3556462521989327042, -8514332474959779238, 3681987062303886320, 1266418540216073989, 4892980044242035752, -5243563662285950589, -8021867029688739836, -5712778566201121978, -2133887347488624783, -667985954315002704, 2350239843243973147, 5123432618264623922, -271741713269398666, 8726020244487579882, 3802883727236102212, 4050625489658817027, 6873081973971784099, -7507676454188557650, -675853520577120389, 4704868291861385417, 1767091830085798988, 1315143445596137295, -8400502078442130692, 4250620495159315861, 7743903342313618441, 8236285998949285411, 920705431865098656, -2187810178560173353, -5636947816335562469, -8869870121412151030],numpy.int64)
        ca(self._r.i64_2, [8621740821050813024, -9092072209079113602, -3056007272962959794, 5895514005284775249, 4825857599917744482, 2093519537988072834, -4390907564722863586, 8598973384036716702, -1889020672280261540, -8273635663381002611, -1941314642980235766, 1812319066748738475, 4190176042918780749, -4555199367311683530, 5467393609117797644, 8359783806563259266, 3800668915803924955, -2655932873935461949, 3136675805239089308, -3633713411557631382, -672757299114219972, 3045962201700775993, -3026485644327632861, -3372272670687649520, 3387661134442604201, 3677140703283269642, 4482422720713908644, 1337692977628619063, 6948420747960198793, -2492903114419653680, -5938903035079054289, -7806446185001452553, 9040686595201532492, -2127381394247868345, 8655785215940696615, 6435851473422996010, -8509497626685383427, 1304836616586909040, -2675436555158709746, 7454381249933066408, 1631169664587044350, 6013206163109033855, -2269271257167747155, 362749191994199052, -2710425314932035541, -3130715904393787670, -4410494504975660198, 4957729582609338569, -8246870151259110017, 6845983371242614475, -2258617392930568184, -8252230642158077029, 2670510062513563636, -6653455225739816423, 3093107250382849352, 1150551445512420048, 1546949923942708166, 5021898317351658427, 3707867854662121111, -1206055501856481918, -1873593186785558123, 6775838224715797812, -1115046710372778769, 528633723916988990, -4174382295242439358, -5547557100483108777, 5731859982382023557, 2204054933203810496, 3007479017130878933, 6608694896063582073, 1503694568421070630, 1248413523206321552, -6401043893159800201, 1353202742204949340, 2304302719445899395, -1291964394378923514, -5522844881206564639, -1277367478728568636, 1849991021787670735, 478721890957105862, 7757247149420834244, -373709650675810738, -5057614129950301004, 6162983513491054102, 3145006736835504836, 5885317631158909353, -7602326138257639761, -4157450027384868646, -1360567824864190920, 229176854089967110, -2202711857284656499, -2946750387084440631, -7399092435233174868, -931278862032913506, 8725183201793225879, 4422438402418122694, 7390489870132742668, 5253764508555093227, 1198113859723757987, 7260998365611273804, 1540767319493735478, -5799740479458549922, 1136167730386243597, 1413668892541509388, -8362134679601352333, 3664237052291625965, -7059531260401496534, 244969021945500288, 7960640458120876383, -2144041369569582147, -8542531942333624037, -6912033525905196529, 7309130333167087960, -1428796488709117140, 7889412153530907816, -6519274351560620428, -7194011194445795971, -2253470711475766161, 2052913415378741465, 8349030699411536987, 2962275883196204755, -8896757719886490153, -3481651114681941922, 9178906373760388169, -2393681984948405823, -4722899724188292419, 2219571189613806132, -8736536710280581263, -6631663654879231430, 1213083601717174358, 351791283162447724, -2728467560827636562, 2174378918144416458, 748751282949822397, 4251372914295826830, -4967177568325109568, 3825916028954041329, 7303839053387841791, 8648996684183789510, -6188350610717327471, -9016026939100696370, 8366545235017906362, -4151061240351591634, -3308165752571595210, 5710967263762362072, -7116887066458274066, 6003026705335466483, -2788076296930402698, -696935785960712847, -3523035848103775545, -4808396779515182120, -4487243801299967856, -316555344628268867, 2148745648896444003, -7908465185551702581, 209478862744791304, 8329349262325078360, 2312897865550480622, 3534430375708664567, -4313813383770928446, 7798388933635693783, 423303070618897314, -6223899204612392666, -7997497118304435999, 1761514773996835425, -8886871075540730292])
        self._r.u64_1 = 1465640522145789825
        if self._r.u64_1 != 13389861970863644378:
            raise Exception()
        self._r.u64_2 = numpy.array([6515978873578326855, 1465640522145789825, 14139647178981527348, 17376225719361197745, 4827355217349405315, 5237172857588412536, 11185863429255124449, 11922950710462888186, 9723873762901963012, 2360891509504070464, 17595800616336901155, 4676383109049523121, 5519403084078587651, 15199794964642249670, 10725748072798711186, 11861452006494413908, 10866242934922922899, 15599520359228044898, 4022505103249338009, 15081262745932646374, 9978655822822015426, 1893338345735521355, 8335612627840221039, 13125076221780371251, 1843608744939432450, 1877855184169582147, 360237399108374165, 14133486497511175136, 6918428392028668980, 4207262405010786686, 11882372330517522341, 2660307236802524516, 16105897257753062921, 2353931053072926625, 10173424970756197713, 3742480367255311168, 1303431584704287527, 12527899890265500372, 32220987555692133, 17556513786877588779, 14599571048880016586, 2017220613051019209, 13580232873699969747, 3864855431338072766, 10522968089599101769, 445176367690966897, 7790111520686478868, 6394442284921113988, 16995884223523288612, 11216569412804039035, 4321418227933556664, 5409834497962741327, 690550291029646943, 16074599988808644612, 11236550486638087434, 6844569081007881849, 5869987636307743707, 7778211196101597376, 15853871901637280370, 18058575643888946512, 14027203060397441285, 12712062502708340258, 4041613882264720796, 11645048579559315688, 1246226537584125354, 3474795601576826029, 11513896830487717539, 1974322205737539934, 17242471345616954213, 8678121572397745114, 17527671945381764646, 5033231148296076497, 6411880965725185093, 174473638020748044, 8158678930583416018, 9507609436552652251, 16205993571484058929, 8035338227846555833, 8791374446603527925, 14595445946451526244, 5169961786923105799, 13397974474224235898, 2364042737119390982, 5321299597050057517, 1121024914655468441, 12207167839097364776, 12619831538472755181, 4864354177058320218, 17848460798228747459, 13261044407690283599, 10209900008497671979, 6862409070349488681, 1432310611369939292, 2092522766869471913, 15058223303172327711, 4178174561433201628, 12906394038648389198, 15191542062580018441, 16452252929507747318, 11201120125455394600, 6726163449083399053, 8426476024479275017, 7026246701397961488, 9033438331677737541, 5951673483825817230, 10638919135849238472, 3252342350133602871, 15766880131631627052, 12385842632184481382, 2748643971592610065, 6396730451340699978, 13659499533346384982, 4282043305472384300, 1711405441567413160, 17992713571449412921, 3556627233283536994, 4138074248161109398, 1622144212241737621, 18087263875532968938, 14104137172003718411, 7644309790031389842, 8816844725250613052, 11421439960737023984, 10454322951672789795, 2119200398037807197, 8384409476347314289, 2527068029837223073, 4862875043870995989, 17581079332542377528, 18385625565005546141, 5262116103886681622, 14174635193688816521, 3985859099523137999, 5526499814203466410, 1239704066545123753, 5917443538249299253, 878138865084935513, 10218107935864045533, 6547939038367120283, 7353731416371741667, 5504609912290331194, 17697030959073472945, 3134771705926671223, 1308908721146697947, 10579235124105673010, 17332984836700322102, 13722665407351335633, 18423215754649979094, 3171161736406578023, 4234709098044006158, 7347564326123203638, 8195365762234651673, 7781698260938130820, 1180819293191049424, 493531138123366511, 1365828412106184272, 10313217779396245974, 7602972172978537794, 6065626025778962290, 9672897350080504270],numpy.uint64)
        ca(self._r.u64_2, [17812699909525330179, 13389861970863644378, 16257896157253761478, 14191477546208115816, 1387441194387183523, 8800889055657239662, 3787113061722336589, 2075067786453142295, 2302772129471114307, 16660993589300385169, 5227667125318999851, 17211198982499914739, 13967365476154884537, 6210802835678950626, 413837793611927178, 15016088479821729126, 14194309003275915218, 5521545037113246785, 9721585675207248367, 2487154057124779480, 4054392452442988950, 15742440468026600431, 8404041348136789525, 5704587169648799325, 8615894037736189999, 7555294940121326684, 166204857340424907, 10630415758080788319, 3699593146963368456, 15841753586674104403, 1425904355269403798, 6757749835782369274, 6484708862168533651, 14311810156028177789, 13305336491678304892, 9547219694933920657, 16939089102075290494, 13780222831094724753, 729578726262763066, 6741605646549400625, 860499368566843233, 4821657628681234936, 10629375059978179469, 12676697982045410789, 7965873501849669898, 6463814633396676710, 10304605129170106831, 17634109250944839532, 7874201956261190767, 2093432098376142516, 15162293521637815459, 14480915389905814968, 12246183009228206627, 9927056522845945393, 10708714764412026102, 12620101894595011829, 9720992984909508434, 1335165052342958298, 3842118717279685369, 5703296853718993513, 10169884007081888934, 2514628960699067131, 5254570865582417565, 9562135776312844762, 27891557900731192, 14886705471885923481, 3399688988254798568, 14640082747632735324, 12221809011211673821, 12865683977160344326, 12797396568995658538, 16277433856161229511, 5834216036130347946, 41836075316600799, 6171722505441450511, 8601242920007887523, 13624814788188880079, 7848598808818978240, 14273686016064474182, 9616131192223535887, 17907341921682029586, 10138262866472100954, 14661185914352643699, 18102813560908894003, 12307841218657619289, 14709882437025014177, 10238864911411793767, 4776457610936466600, 8782354639535937976, 18274481696525890320, 13992637006136445380, 11566349649437476293, 1209664843394078754, 14394522101288007152, 2915009092315033094, 182528511086129450, 15695741318843217573, 744918667092745933, 7146826536782008676, 13838640680680387773, 6708462726963541522, 7741352156378706754, 15062394166759350529, 10613549923461193838, 11002287295489384645, 11112868002985992483, 14972199425906445655, 15176061787056984512, 3369667758791907709, 10545737311162535909, 10549452773932875360, 977025607559254534, 8213649184128301518, 16026014660753415782, 16346803042848708719, 8641570190583236526, 10372374375551503871, 8475065376071450531, 9492316019190861724, 7258336917778003543, 7704933404615957344, 14492234026024540236])
        self._r.str1 = "Hello Server!"
        if self._r.str1 != "Hello Client!":
            raise Exception()

        #The rest doesn't really matter for numpy testing
        return


        #More complex stuff in the testing of properties
        s1 = self._r.struct1
        ca(s1.dat1, [2.416507e+16, 4.573981e-21, 3.468194e+10, -2.393703e-06, 4.937973e-15, 4.706768e+14, 4.286830e-10, -1.090462e-14, 2.238670e+03, -1.254407e+14, -1.275776e-21, -4.124599e-10, -4.953108e+11, 2.808033e+03, 4.685151e+14, 3.710607e-08, 3.523588e-01, -5.585682e-20, -3.290719e+08, 1.600972e+17, 4.257210e+16, 1.114490e+04, 2.739939e-10, -4.332717e+16, 3.482223e+00, -2.162451e+10, -4.527774e-04, 8.558987e-19, 3.755463e-12, 3.863392e-08, -8.351348e-05, 4.774283e+02, -4.612524e-06, 2.206343e-06, -2.767520e-17, -4.183387e+08, -2.037466e-19, -1.780912e-18, 1.656909e-07, 4.799751e+07, -3.604348e-06, -3.146762e+08, -3.709450e+15, -2.379431e-09, -3.034066e+05, -3.072796e+01, -1.057111e-14, 4.753235e+07, -2.725014e+07, -4.895406e-20, 5.339502e-20, 9.375211e-11, 1.632454e-03, 1.051386e+01, 1.915580e+17, -1.999453e-09, -3.087190e-02, -3.222377e+15, 4.219576e+03, -1.401039e+05, 3.950473e-15, -1.620577e+10])
        if s1.str2 != "Hello world!":
            raise Exception()
        if len(s1.vec3) != 3:
            raise Exception()
        if s1.vec3[1] != "Hello Client!":
            raise Exception()
        if s1.vec3[2] != "Hello Client, again":
            raise Exception()
        if s1.vec3[4372] != "This is yet another test string":
            raise Exception()
        if len(s1.dict4) != 3:
            raise Exception()
        if s1.dict4["teststring1"] != "Hello Client!":
            raise Exception()
        if s1.dict4["teststring2"] != "Hello Client, again":
            raise Exception()
        if s1.dict4["anotherstr"] != "This is yet another test string":
            raise Exception()
        ca(s1.struct1.mydat, [-2.457273e-05, -3.349504e-13, 4.139542e-09, -3.944556e+04, 2.761296e+04, 8.570027e+16, -2.472613e-03, -2.096009e+03, -4.186716e+10, 4.584716e-20, 3.951344e-03, 4.557915e+05, -7.117988e+03, -4.605957e+11, 7.353630e-10, -3.303575e-19, 6.133982e+05, 4.528668e+01, -1.427778e-11, -3.509465e+15, 1.695706e-04, 1.732872e+14, -6.370107e+01, 3.269065e-06, 4.480613e+03, 2.058970e-06, -3.748223e+05, -1.507989e-09, 1.690251e+19, -2.177567e-08, -2.391641e+16, 3.617128e+03, 2.568296e+15, -3.009031e-07, -3.754976e-09, 2.458890e-06, -3.800108e-11, 1.555663e-11, -2.085887e+18, 8.574830e-22, -7.228491e-13, -3.987643e-10, -4.777544e-02, 3.908200e+04, 4.221779e+11, -7.528852e+06, -2.077042e-19, 4.478813e-02, 3.506975e-06, 1.011231e+12, -2.181961e+17, -5.098346e+16, -3.791130e+06, -2.734203e-14, 6.340994e-13, -4.582535e+07, 3.977645e-06, -3.785260e-07, -4.102542e+06, 4.751411e-16, 4.203566e-14, -3.894958e+00, -4.585783e-14, 2.432993e+15, -3.592680e+14, -1.560186e-12])
        if len(s1.dstruct2) != 2:
            raise Exception()
        ca(s1.dstruct2["test1"].mydat, [3.785355e-17, -2.518001e+17, 4.016500e+08, 6.566648e-04, 1.284318e+07, -2.674821e-13, -4.955749e-14, -1.699098e+00, 2.901400e+05, 1.499143e+13, -2.252822e-05, -2.653172e-14, -2.482811e+07, 2.353638e+18, -2.177258e+17, -4.715112e+06, 4.508858e-18, 1.205611e+17, -3.469181e+00, 2.383792e-13, 4.544766e+14, -3.029250e-05, -2.545049e+05, 3.149303e+19, -3.724982e-10, 4.066723e-02, 2.809941e-08, 1.279689e-20, -3.303471e-09, 1.846558e+08, 1.311495e-06, -1.185646e+04, -2.603100e-19, -3.519314e-17, -1.595996e+04, 9.735534e-20, 1.234003e-04, -9.697458e+08, -4.895883e-02, 4.770089e-16, 3.757918e-11, 5.253446e+18, 5.071614e-13, 3.793300e-08, -1.993536e+12, -1.846007e-11, -3.458666e+03, -3.995887e-10])
        ca(s1.dstruct2["anothertest"].mydat, [4.856615e+15, 5.981566e-22, 1.433616e+14, 1.747102e-09, 2.850376e+06, -3.748685e-08, -4.969544e-21, 2.530419e-01, 4.393913e-09, 3.837331e+04, -4.315065e-04, -1.073834e-17, 1.244057e-15, 3.901853e-10, -2.725237e+10, 2.896243e-18, 3.609897e-13, -1.937982e+02])
        ca(s1.multidimarray.Dims, [10, 10])
        ca(s1.multidimarray.Real, [3.489074e-03, 4.416440e+12, 1.069372e+12, -3.678917e+01, 3.617865e+03, 2.631290e+07, -1.012036e+06, -4.990820e+01, -4.607768e+10, -1.205544e+18, 3.384829e-05, -2.739955e+12, 4.098031e-13, 2.170650e+15, 3.313171e-07, -1.107813e-03, -4.840364e+09, 3.470747e-08, -2.945301e-13, 4.900611e+00, 2.494936e-11, -3.705569e-06, 1.189413e-03, 3.034111e+08, -4.905472e-17, -3.857051e-07, -2.096687e-19, -1.795052e-06, 2.523800e-18, 7.860593e-02, 3.519022e-16, 1.236777e+12, 2.636618e-10, 4.386448e-06, -2.513132e+03, 1.400490e+18, -3.156777e+15, 1.661838e-07, 1.652002e-01, 3.732142e-17, -2.562672e+10, -1.965676e+08, -5.664540e-01, -3.224055e-17, -2.842033e+18, 4.816053e+11, 2.517680e-08, -6.443991e+02, -4.267612e-21, -3.524623e+02, 3.760018e-10, 1.060012e-06, -4.158190e-01, -1.969302e+14, -3.838685e+16, 4.574934e-09, -2.832637e-09, 1.005947e+06, 2.388806e-15, 2.331301e+15, -4.602999e-13, 1.987431e-20, -2.190281e-03, 3.648919e-08, 7.198137e+07, 1.772828e+02, 3.444774e-20, 6.255538e+07, -2.058346e-02, 6.081334e-02, 4.300420e+12, -7.901606e+03, 9.496649e-13, -2.206441e+09, -4.628939e+00, 1.660493e+01, -3.623921e-09])
        if s1.var3.data != "This is a vartype string":
            raise Exception()
        s2 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct1",self._r)
        s2.dat1 = [1.139065e-13, -1.909737e+06, 2.922498e+18, -1.566896e+15, 3.962168e+17, -3.165123e+17, -1.136212e+13, 3.041245e+16, -4.181809e-18, 3.605211e-18, -3.326815e-15, -4.686443e+05, -1.412792e+02, -3.823811e-14, -6.378268e-09, 1.260742e-14, -2.136740e-16, -4.074535e-10, 2.218924e+01, -3.400058e-08, 2.272064e+02, -2.982901e-21, 4.939616e-19, -4.745500e+03, -1.985464e+16, 3.374194e-04, -8.740159e-09, 1.470782e-06, -2.053287e+06, 4.007725e-13, -1.598806e-13, 2.693773e-06, -3.538743e-08, 4.854976e-16, -4.778583e-12, 3.069631e+06, -3.749499e+03, 3.995802e+05, -2.864014e+13, 1.276877e-13, -4.479297e-02, -9.546403e-13, 8.708525e+06, 3.800176e+04, 4.147260e+10, 2.252187e-20, 9.565646e-14, 4.177809e+13, 3.032250e+01, 3.508303e+10, -4.579380e-17, 1.128779e+05, -1.064335e+11, 1.795376e-06, -1.903884e+09, 2.699039e-03, 3.658452e+15, 4.534803e+15, 1.366079e-03, -3.557323e+07, -4.920382e+18, -3.358988e-07, -4.024967e-11, -4.784915e+16, 1.490340e-18, -4.343678e+08, -1.955643e+14]
        s2.str2 = "Hello world 2!"
        s2_3 = {}
        s2_3[10]= "Hello Server!"
        s2_3[11]= "Hello Server, again"
        s2_3[46372]= "Test string!"
        s2_3[46373]= "Test string again"
        s2.vec3 = s2_3
        s2_4 = {}
        s2_4["cteststring1"]= "Hello Server!"
        s2_4["cteststring2"]= "Hello Server, again"
        s2.dict4 = s2_4
        s2.struct1 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2",self._r)
        s2.struct1.mydat = [1.783093e+12, -2.874045e-19, -2.311319e-19, -3.099234e-12, 1.000951e+16, 3.775247e-12, -5.853550e-18, 3.175537e-10, -3.112089e+08, -1.577799e-06, -1.379590e+00, 4.777044e+13, 4.811910e+18, 4.736088e-11, 1.770572e-08, 2.713978e-22, -1.649841e-12, -2.486590e+10, 4.092716e-18, 8.724120e-03, -1.183435e+18, -3.904438e+08, -1.251365e-11, -4.007750e+19, -2.206836e-16, 4.014728e-13, -3.960975e-12, 7.192824e+05, 1.981836e+04, 1.840814e+16, 1.488579e-16, -4.862226e-06, 1.612923e-17, -4.978203e-04, -2.305889e-02, 7.627221e+13, 4.014563e-03, 2.388221e-03, -1.129986e-02, 4.055276e+10, 3.842121e-10, -8.588514e-04, 1.299077e-12, -3.331850e-12, 4.863277e-01, -2.250328e-11, -2.261245e+04, -2.770899e+09, -4.710672e-15, -2.267765e+06, 1.582168e-09, 3.664505e-06, -1.507921e+12, 5.460120e+09, -3.256706e-15, 3.012178e-12, 2.274894e+15, -9.664342e-18, -2.770443e-15, -1.955281e-06, 4.768349e+01, -7.679375e-19, 2.774544e-17, -4.928044e-17, 7.602063e-15, 2.506718e-12, -2.794058e+11, 4.329292e+03, -4.041289e-02, 4.035282e-19, 8.577361e-04, 4.197333e-18, -3.509270e-01, -1.711871e-12, 4.578825e-02, -8.783497e-13, 3.862885e+17, 4.219735e+13, 4.281035e-21, 3.323068e-03, 4.931847e-11, 4.032955e-21, -4.373013e-03, 1.592633e-16, -4.484112e-16]
        s2_ds2 = {}
        s2_ds2_1 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2",self._r)
        s2_ds2_1.mydat = [4.122753e+13, -2.656829e-13, 1.813864e-04, -4.675181e-05, 1.759511e-19, 3.517805e+10, -7.912215e+01, 7.708557e-07, 2.434017e-21, -2.540544e+00, -9.412568e+15, -2.124215e-18, 2.797799e+13, -2.240464e-07, 2.780110e-12, -1.025574e-14, -3.762272e-09, -5.715981e-02, 1.839704e-21, -4.719538e-15, 3.148156e-06, 3.483886e-12, 3.484006e-02, -4.544817e-08, 3.200642e+00, 4.503141e+07, -4.077123e+04, -2.776985e+00, -2.900651e-18, -1.463711e+08, -3.460292e-03, 2.348911e-18, -3.704219e+08, -3.275364e+05, 4.613595e-01, 4.867108e+16, 4.114866e-10, 3.070767e+17, 4.662623e+01]
        s2_ds2["ctest1"]= s2_ds2_1
        s2_ds2_2 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2",self._r)
        s2_ds2_2.mydat = [-1.037656e+15, -3.782364e-06, 4.982303e+06, -5.510401e-07, 4.271118e-02, -1.718093e+11, -2.644457e+01, -2.374043e-08, 1.729038e-14, 3.370840e+10, 4.302550e-13, 2.643402e+14, 3.199649e+01, 4.620204e-08, 1.323645e+00, -4.337167e-07, -5.003428e+11, 4.176127e+13, 3.324907e-09, -4.207938e-09, -3.324360e-15, 3.317889e+00, 1.775668e+07, -1.295276e-15, -1.610388e-05, 3.417067e-02, -4.874588e+04, -2.109628e+12, 3.130648e+09, 1.898554e-13, 2.421724e-01, 4.227281e-08, 4.844407e+19, -4.490481e+10, 2.599780e+00, 4.039296e+06, -2.944167e-03, -7.388370e+08, -4.473409e-02]
        s2_ds2["anothertest"]= s2_ds2_2
        s2.dstruct2 = s2_ds2
        s2.multidimarray = MultiDimArray([10, 10], [2.607856e-05, -4.060588e-01, 1.459089e-19, 7.661488e+12, -3.054205e+15, -3.953672e+18, 3.981083e-09, 2.023530e+10, 3.341041e-21, 3.927871e-04, -4.843469e+01, 2.836056e-20, -3.148469e-04, 2.672701e-06, 3.588983e+08, 2.702981e-17, 4.366455e-06, 1.595520e+11, 3.130938e+09, 4.453168e+10, 9.627982e-12, -3.824527e-11, 4.172935e-20, 6.284725e+03, -9.490302e-13, -2.151807e+18, 2.926671e-02, -1.089334e+02, 2.671842e+17, 2.174924e+06, -1.772301e-19, -1.809115e+08, 3.058543e-06, -1.098521e-18, -7.276741e+01, 6.617143e-22, 2.181270e-03, -4.632712e+08, 1.067154e-11, -1.149804e-12, -2.883778e+07, -2.772835e-15, -7.289469e-04, -2.053436e-01, -4.477369e-19, -4.906893e+10, -3.005378e-02, -7.615476e+07, -9.075230e-20, 3.684300e-04, 2.884596e-05, 3.589573e-06, 3.938783e+11, 2.541751e-08, -6.447446e+09, -8.709398e-02, -9.877435e-20, 1.430333e+14, 1.961905e-17, -4.892539e-05, 2.650625e-02, -4.408943e+01, 2.800706e-20, -1.087373e-03, -1.081200e-03, -3.748735e-10, -4.052447e+03, -1.102631e+02, 6.629702e-17, -1.349501e+10, -3.396688e+03, 1.492315e-01, -3.770557e+07, 4.248273e+11, -5.822309e-02, -2.695009e+18, -2.544586e+16, -2.923482e-20, 2.842902e-08, 2.007452e+00, 1.684762e-04, -4.948805e+14, -3.964645e-16, 4.261808e-05, -2.513086e+17, -1.863688e+01, 2.786936e+17, 2.306164e-12, -4.813284e-02, -3.734933e-15, 1.986399e-02, -2.682815e-14, 2.293712e-07, 1.247696e-01, -2.455383e+19, 2.697551e-09, 1.274751e+09, 2.041100e-15, 6.322583e-08, 3.443236e+00])
        s2.var3 =RobotRaconteurVarValue( [6.404176e-12, 9.258110e-03, 8.657620e-03, -2.064381e+00, 5.182360e-16, 4.167658e-16, -4.533051e-19, 5.357520e+18, -4.990383e-13, 2.286982e+08, -4.727256e-18, 1.465299e-17, 3.000340e-10, -2.304453e-04],"double[]")
        self._r.struct1 = s2
        s3 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2",self._r)
        s3.mydat = [-1.451096e-09, -3.762302e-18, 2.016877e+04, -4.171245e+16, 1.500851e+09, -3.071385e-05, 1.329949e+09, 9.439580e-14, 8.652806e-06, -2.729712e-17, -1.664008e-09, 3.787440e-16, -4.281157e-20, -8.703642e-07, 7.130173e-13, 1.162347e-04, -2.485922e-01, 8.924836e+13, 2.150995e+18, -1.816269e-08, 3.572064e-06, -1.020374e+19, -2.467612e-05, 1.294111e-21, 3.030328e-11, 1.736324e+04, 4.221306e+17, -2.544109e+09, 1.047630e-04, 2.082666e+04, -4.120572e-04, -4.550228e-11, -4.959645e+00, 3.988634e-06, -2.901463e-06, 4.379435e+14, 3.697324e+17, -3.285280e+00, -4.491892e-21, 4.962405e-03, -4.143004e-05, 4.447309e+01, 3.196998e-04, -1.679927e+06, -1.859794e+19, -2.749978e-17, -9.042867e+14, 3.970588e+06, -2.359863e-19, 4.923781e-03, 3.689224e-03, 1.741368e-14, -4.943555e-15, -2.473041e-09, -1.687125e-12, 4.622096e+17, 2.456838e-17, -4.076597e+07, -4.082942e-21, -4.483141e+19, 2.463502e-01, -1.818087e+04, 1.094518e+14, 7.514618e+03, -1.175704e-07, -3.071050e+18, -8.006996e-20, 1.363550e-14, -6.753529e+08, -4.661760e+15, -2.475629e-01, -1.282411e+16, -6.328699e-04, 4.898115e+00, 6.921801e-14, 9.951973e+01, 1.669967e-08, -3.750408e-19, -3.363050e-10, -2.470083e-09, 1.544354e-05, -2.844838e-09, 4.426875e+02, 3.468203e-17, -2.376018e+07, -1.431106e+08, -6.900572e-18, -4.640801e+07, 9.947893e+14, -1.166791e+10, -3.478840e+19, -3.103020e-09, -3.256701e+00, 4.374203e-14, 4.655054e-04, -4.106246e-17, 2.373568e+15, -1.319790e-04, 1.485607e+02, -4.933523e-05]
        self._r.struct2 = s3
        s4 = self._r.struct2
        ca(s4.mydat, [-4.415088e+16, -2.033093e-17, 3.634431e-17, 2.030794e-03, 4.464343e-14, -4.137056e+11, 3.609991e-16, 4.332970e-11, 1.327470e-06, -3.304680e+02, 3.184654e-08, 1.194960e-16, -2.958549e+05, -3.320274e+13, 3.486845e-05, 2.878185e-10, -2.982726e-12, -3.653410e-06, 2.059068e+00, 1.150498e+16, -3.647068e+18, -3.847760e+03, -4.333684e-21, -2.357376e-07, -2.560470e-09, 2.931250e-15, 4.966713e-21, 2.960478e-14, -1.959583e+03, 4.593629e-16, 4.193491e-07, 5.941674e+14, 2.198075e+05, 1.487817e-20, -4.643292e+06, 2.543864e-14, 9.478332e+04, 2.948237e+13, -3.144190e-17, -1.369134e+11, -4.908672e-18, -3.581399e-21, -1.682968e-14, -8.984437e-02, 3.067043e-19, -3.361220e+14, -2.591105e-10, -2.119291e-13, 7.649594e+03, -1.869427e-01, -3.403057e+11, -4.798229e-09, -4.120069e+04, 3.384741e-12, 4.697254e-10, -3.594572e-02, -1.973059e+12, -2.627069e-21, 4.096077e-20, 1.629242e-20, -1.561816e+11, 3.240449e+07, -3.967391e+08, 4.635131e-14, -3.436364e-17, 1.485817e-15, -2.145973e+18, 1.160688e+19, 3.266439e+11, 1.686854e+02, -4.048943e+00, -2.905109e+17, -3.953827e+15, -2.855712e+10, -1.197294e-02, -1.997014e+14, 3.951602e+08, 1.287972e+18, -4.228933e+08, 4.212816e-06, -1.252397e+15, 3.517842e+12, -3.315039e-17, -1.816738e+19, 3.595783e+14, -2.834015e-08, 3.436611e+04, -4.192603e+12, 1.152454e+11, -9.405739e-21, -1.862898e+17, -3.811397e-10, 4.486272e+00, 3.666408e+14, -2.681908e-10, -4.859125e+08, -3.593152e+04, -1.883343e-03, -2.445939e-08, 4.540371e+01])
        is_d1_1 = self._r.is_d1
        if len(is_d1_1) != 3:
            raise Exception()
        if is_d1_1[9285] != 1.643392e-01:
            raise Exception()
        if is_d1_1[74822] != 1.537133e+09:
            raise Exception()
        if is_d1_1[4] != 1.369505e-03:
            raise Exception()
        is_d1_2 = {}
        is_d1_2[928]= 4.074501e-07
        is_d1_2[394820]= -4.535303e+05
        is_d1_2[623]= -2.956241e-20
        self._r.is_d1 = is_d1_2
        is_d2_1 = self._r.is_d2
        if len(is_d2_1) != 2:
            raise Exception()
        if is_d2_1["testval1"] != -1.079664e+16:
            raise Exception()
        if is_d2_1["testval2"] != 2.224846e+00:
            raise Exception()
        is_d2_2 = {}
        is_d2_2["testval3"]= 5.242474e+10
        is_d2_2["testval4"]= 2.208636e+08
        self._r.is_d2 = is_d2_2
        is_d3_1 = self._r.is_d3
        if len(is_d3_1) != 2:
            raise Exception()
        ca(is_d3_1[12], [8.609080e-13, 3.946603e+03, 2.994203e-10, 3.200877e+14, 1.747361e-09, 2.827056e-16, -3.676613e-18, 1.886901e-14, -9.970511e-12, 1.932468e-18, -3.629253e-05, 4.903023e-12, -3.919949e-10, 4.982164e+07, 3.823096e-20, -4.044068e-13, 3.114078e+09, 7.572697e-12, -2.619929e+04, -3.882046e+01])
        ca(is_d3_1[832], [4.750899e+00, 3.924377e+18, -2.735066e+17, 4.095362e-21, -2.407932e+09, 4.059499e+10, 1.376975e-10, -8.547220e-21, -1.344568e-20, 2.809398e+03, 2.118944e-06, 2.435328e-03, -1.410999e-12, 9.907226e-04, -9.745948e-20, 1.270118e+15, -2.833333e+05, 1.032636e-10, 5.312574e+13, -2.651512e+02])
        is_d3_2 = {}
        is_d3_2[47]= [4.335907e-08, -3.270294e-03, 1.752801e-01, 1.235219e-20, -4.348647e+02, -4.503864e-21, -3.316231e+15, -2.080056e+17, 1.813854e+13, -3.380846e-05, 4.350998e+03, 4.539570e+11, 8.981827e+09, 3.326114e+01, 2.975688e+06, -1.017456e-12, 2.989498e-03, 2.842392e-03, -1.258677e-21, 1.068563e-15]
        is_d3_2[324]= [3.239279e+12, 1.047689e+17, -1.236114e+17, -4.002822e-17, 2.657374e-03, 7.383907e-19, -5.067889e-13, -4.195122e-12, 3.642885e-01, -2.946040e+14, 5.522403e-08, 6.603132e+04, 1.464154e+05, -1.851534e-08, 2.808294e-13, -2.702278e-11, 3.850704e-06, -2.453957e+02, -3.015401e-02, 1.654070e+05]
        self._r.is_d3 = is_d3_2
        is_d4_1 = self._r.is_d4
        if len(is_d4_1) != 2:
            raise Exception()
        ca(is_d4_1["testval1"], [1.113851e-04, 3.830104e+07, 4.571169e-21, -4.064180e-05, 2.889736e+01, -1.790060e-06, 4.608538e+00, 4.687713e-04, 1.387717e-08, 3.914187e-18, -5.618118e-06, 1.530811e+05, -5.848922e-11, -3.397558e-20, -6.597368e-08, -3.779049e-06, 2.406033e-19, 2.507939e-10, 3.246113e-20, 1.341205e+16])
        ca(is_d4_1["testval2"], [-3.088190e-13, -4.033334e-20, 4.150103e-21, -6.610855e+17, 3.688824e-13, -3.208025e+13, -5.034888e-11, -4.098363e-06, -1.272830e-03, 2.748392e-03, -2.644272e-06, -4.810065e-18, 4.629861e-19, -5.444015e-03, 4.046008e+17, -3.548079e+12, -3.455290e+16, -3.668946e-12, -3.522178e-01, -1.537583e+14])
        is_d4_2 = {}
        is_d4_2["testval3"]= [1.771838e+06, 3.037284e-01, -1.739742e-02, 1.399508e-20, 3.605232e-21, 3.517522e+14, 4.887514e+14, 3.505442e-03, -3.968972e+18, 1.422037e-20, 2.596937e-21, 4.852833e-11, 6.852955e-17, 4.765526e-12, -3.445954e+16, 2.322531e-14, -1.755122e-12, 3.941875e+00, 8.877046e-13, 2.818923e-02]
        is_d4_2["testval4"]= [4.146439e+16, 2.923439e-07, 3.549608e+16, -1.664891e-01, -4.192309e-15, 3.857317e+05, -1.101076e+00, 1.213105e+19, 3.237584e-14, -2.421219e-06, -4.603196e-05, -3.719535e-10, 1.124961e+06, 2.032849e+10, 4.639704e-22, 3.946835e+01, -9.267263e+01, -4.456188e+11, 3.470487e+08, 7.918764e+10]
        self._r.is_d4 = is_d4_2
        is_d5_1 = self._r.is_d5
        if len(is_d5_1) != 1:
            raise Exception()
        is_d5_1_1 = is_d5_1[564]
        ca(is_d5_1_1.Dims, [10, 10])
        ca(is_d5_1_1.Real, [-2.240130e+14, 1.609980e+16, -1.794755e+07, 8.108785e+17, -2.296286e+08, -2.689029e+13, 2.036672e+07, -4.822871e-02, 4.070748e-05, -2.894952e-04, -1.728526e+17, 4.077694e-19, -2.977734e+13, -9.428667e+03, 2.672315e-08, -1.844359e+19, 4.243010e+09, 4.592716e-01, -3.792531e+10, 3.117892e+04, -1.830821e-16, -3.702984e-18, -1.957300e+12, 9.017553e+12, -2.184986e-17, 1.436890e-02, 4.008279e-12, -2.407568e+10, -3.170667e-07, -2.315539e+16, 6.646599e+09, 2.443847e-01, 1.928730e-21, 3.089540e+00, 2.813232e-02, 1.352336e-21, -3.562256e+05, 3.778036e+08, -3.726478e-13, 3.112159e+15, 3.573414e+17, 3.607559e+09, -2.923247e-19, -2.079346e+14, -4.611547e-16, 2.200040e+00, 3.670772e+07, -4.176987e-20, 2.086575e+06, -2.388241e+01, -3.759717e-19, -2.232760e-01, 9.066157e-21, 2.797633e+07, 3.455296e+00, -3.306761e-08, -2.062866e-22, -4.653724e+07, -3.694312e-17, 2.254095e-06, 3.519767e-16, 1.292737e-06, -3.840896e-08, -1.946825e-20, 2.639141e+18, 3.021503e+07, -1.834066e+18, 4.474920e-02, 3.005033e-20, -1.233782e-10, -3.260111e-08, 2.326419e-09, -2.298222e-19, 7.554873e+15, 2.378479e+19, -5.092127e-03, -4.724838e-07, 3.204184e+06, 2.713748e-12, 1.574309e-05, 6.622323e-01, -4.944461e-01, -1.559672e+19, -3.350494e+15, 2.467451e-14, -4.881873e+13, 1.031263e+15, -4.051814e+12, 1.418548e+07, 1.204368e+17, -4.113152e-02, -4.472069e+16, 4.896886e-14, 2.371633e+05, 3.543019e+04, -3.083516e-22, 1.041761e-09, -2.579812e-06, -2.937567e+09, -4.775349e-16])
        is_d5_2_1 = MultiDimArray([10, 20], [2.792909e-01, 6.554477e+16, 4.240073e-13, -4.490109e+19, 5.410527e-22, -2.244599e+17, -2.656142e-02, -3.819500e+13, -7.086082e-02, 7.790729e-13, 3.375900e-12, -6.915692e+09, -2.900437e-18, 1.257280e+05, -3.810852e+15, -4.589554e-12, 2.670612e-14, 4.725686e+06, -3.018046e+07, 2.439452e+07, 2.726039e-07, -2.805143e+02, -1.870376e+03, 4.573047e-06, 1.904868e+19, -1.966383e+00, 3.426469e-11, -1.400396e+13, -1.724273e+09, -7.347198e+10, -4.081057e-12, -3.868203e+10, -2.686071e+13, -5.289107e+01, -5.574151e-09, -2.580185e-06, -8.222097e-21, -4.957833e-12, -2.491984e+03, -7.900042e+16, -4.809370e-11, -2.048332e-19, 4.984852e-21, 1.350023e+13, -4.492022e-11, -3.255594e+10, 1.495149e-09, -7.272628e+02, -4.236196e-04, 4.736990e-02, -4.030173e-11, 1.017371e+11, 1.124559e-09, 4.177431e-21, 1.026706e+06, -4.702729e-04, -2.633498e+18, -4.689724e+08, -2.593657e+05, 3.433194e-18, -1.977738e-13, -1.163773e+03, 3.424738e-20, 7.391132e-06, 1.364867e+12, -7.155727e+16, 3.078093e-21, -3.151787e-04, -4.715633e+06, 1.017894e+19, -1.121778e+14, -3.529769e-10, 4.530606e+19, 3.988296e-17, -3.469818e+06, 1.204304e+03, -1.404314e+15, -1.369871e+04, -2.796125e-03, -4.842068e-06, -2.639632e-03, 1.324740e+08, 1.440651e+07, -4.778885e+03, -4.643859e+06, 1.726955e-09, -8.160334e+05, 3.763238e+13, 1.391028e+02, -4.269393e+04, -2.698233e+02, -3.677556e+14, 1.070699e-17, 3.949376e+19, 4.503080e-06, 4.344496e-07, 1.714091e-19, -3.436426e+01, 4.914505e+15, -1.101617e+09, -1.899511e-04, 2.195951e-06, 2.402701e-12, 1.783431e-09, -7.329137e-08, 4.423889e+16, 2.812547e-19, -7.848554e+05, -3.635151e+13, 3.128605e-09, -2.858963e+08, 2.086065e-11, -2.544450e+12, 1.450579e+19, -1.508905e+13, 4.307174e+00, 1.038108e-05, 4.313281e-05, 3.647351e+05, 1.309105e-16, 4.180469e+13, -2.701332e-07, -4.033566e+14, -3.116748e-06, 2.342296e-07, 1.870335e-19, 2.312273e+01, -4.478923e+08, -4.854324e+09, 2.681828e+03, -4.280128e-01, -4.690703e-21, 3.853815e+16, 1.366639e+02, -2.944985e-11, -4.486958e-13, 3.017750e-11, 3.551437e-13, 2.263828e-12, -6.545014e-18, -7.552023e+12, 7.595238e+14, 2.810247e+12, 6.516008e+15, -3.035786e+14, 2.523040e+11, -3.766603e+09, 7.316287e+18, -2.147132e+17, 1.972210e+10, 2.906768e-13, 4.226577e-14, -2.640568e+17, 2.181408e+10, -1.043256e-08, -3.649181e+06, -2.776638e+18, 3.660147e-07, -1.415433e-17, -4.945127e-17, 2.655050e+01, -2.269828e+04, -2.585499e-01, -3.299965e+05, 3.707494e-18, -1.257923e-19, -1.321880e+14, -1.815888e-12, 9.366926e-09, 1.024923e-14, 4.494907e+04, -2.596971e-20, -3.403446e-12, 1.537084e+17, -3.850430e-17, -4.821759e+05, 4.255435e-20, -1.016978e-16, 1.430658e-09, -3.696861e-14, -4.427905e-19, -1.999724e-09, -3.489402e-06, -4.677864e-03, 1.246884e+13, -4.458271e-19, 3.551905e-04, -4.458221e-20, -3.472033e+01, -1.745714e+08, 4.396891e+03, 4.345767e+02, -1.800116e+05, -1.217318e+00, 3.605072e-08, 1.306109e-09, -2.798295e+16, 4.387728e-13, -3.284039e+11, 3.424124e+17])
        is_d5_2 = {}
        is_d5_2[328]= is_d5_2_1
        is_d6_1 = self._r.is_d6
        if len(is_d6_1) != 1:
            raise Exception()
        is_d6_1_1 = is_d6_1["testval1"]
        ca(is_d6_1_1.Dims, [5, 10])
        ca(is_d6_1_1.Real, [4.229153e+02, 3.406523e+03, -2.158208e+15, -7.464845e+07, -4.763504e+18, 6.777497e-20, -1.265130e+18, 2.145141e+12, -8.473642e-18, -3.780104e+17, -4.356069e+06, 1.199990e+04, -2.413259e+07, -2.609077e-12, -2.121030e-16, -1.224176e+09, -2.836294e-15, -1.975701e-18, 4.311314e-04, -4.932020e-20, -1.307735e-18, -4.000536e+02, -1.718325e+15, -3.493595e+05, 1.707089e+00, 4.416780e+01, -1.152954e-13, 8.396437e-02, -4.304750e+16, 1.154166e+02, -2.331328e-02, 4.821737e-04, 5.831989e-20, -6.887913e+06, -1.592772e+11, 4.730754e-19, 2.543760e-17, -5.864767e+14, 2.077122e-13, 2.801695e-12, -1.171678e+12, -8.854966e+18, -1.555508e-08, 3.589410e+11, -1.495443e-21, 2.876586e-06, -2.265460e-03, 2.544109e-03, 2.019117e-06, -6.458547e-21])
        is_d6_2_1 = MultiDimArray([8, 10], [2.080438e+03, -2.901444e-01, 2.561452e+12, 6.760682e+14, -2.461568e-10, -4.811907e-20, 6.299564e+11, -2.660066e-19, 4.643316e+13, 3.292265e-13, 1.187460e+19, 3.054313e-07, 3.503026e-20, -1.465147e-08, 3.993039e-17, 2.469296e-10, -4.014504e+07, 1.810733e+17, -3.976509e-19, -9.166607e+15, 1.854678e+02, 2.884879e-12, -4.382521e+14, 3.064407e-05, -9.542195e+07, -3.938411e-13, -2.850416e-03, 3.042038e+14, 1.464437e-12, -1.550126e-06, 4.938341e+11, -3.517527e+19, 3.135793e+19, 1.380313e-14, -1.060961e+18, 2.833127e-10, -1.862230e+02, -2.232851e-05, 4.773548e-05, 3.746071e+13, -4.972451e+09, 4.553754e-14, -8.183438e+10, 3.739120e+18, -1.619189e+19, 4.644394e+08, -8.327578e-11, 4.080876e-02, -2.806082e-03, -1.595033e-06, 1.973067e+16, 2.989575e-07, -8.974247e+15, -4.204211e-03, 1.513025e-02, -4.604953e+03, 4.107290e+16, -3.631920e+12, -1.902472e+13, -4.186326e-14, 2.465135e+13, 5.060414e+12, 7.508582e+11, 3.233186e-14, -6.750005e+14, -9.467336e-16, 2.101440e+03, -1.162425e+08, 7.808216e+04, 4.356208e-19, -3.316834e+14, 3.299774e-19, -3.746431e-16, -3.971172e-07, 2.423744e+10, 1.542747e+17, 2.358704e-05, 4.201668e+17, -3.736856e+07, 3.585645e-07])
        is_d6_2 = {}
        is_d6_2["testval2"]= is_d6_2_1
        self._r.is_d6 = is_d6_2
        is_str1_1 = self._r.is_str1
        if len(is_str1_1) != 1:
            raise Exception()
        if is_str1_1[23] != "Hello server":
            raise Exception()
        is_str1_2 = {}
        is_str1_2[24]= "Hello client"
        self._r.is_str1 = is_str1_2
        is_str2_1 = self._r.is_str2
        if len(is_str2_1) != 1:
            raise Exception()
        if is_str2_1["testval1"] != "Hello server":
            raise Exception()
        is_str2_2 = {}
        is_str2_2["testval2"]= "Hello client"
        self._r.is_str2 = is_str2_2
        is_struct1_1 = self._r.is_struct1
        ca(is_struct1_1[748].mydat, [-9.692618e+00, -1.944240e+03, -2.456327e+16, 4.673405e-20, 5.147581e-14, -3.773975e+15, 2.336430e-21, 1.597144e-18, -2.609059e-03, 3.557639e-21, -1.666575e-16, -4.242788e-07, 2.686206e+07, -3.200902e-05, -1.549754e-06, -3.010796e-12, 4.638418e+01, 2.664397e-14, -2.689174e+01, 4.564584e-21])
        is_struct1_2 = {}
        is_struct1_2_1 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2",self._r)
        is_struct1_2_1.mydat = [-2.101948e-07, -2.594836e-08, 2.515710e+01, -3.834127e-14, -3.088095e+06, -3.256612e-02, -1.855481e-19, 3.801916e+07, 2.145894e+09, 4.487676e+12, 1.351202e-02, -1.125124e-16, 1.369826e-20, -2.290673e+00, 1.786029e-20, -4.991515e+08, 4.006107e-10, -4.947871e-11, -2.737020e-08, 4.123759e-20]
        is_struct1_2[372]= is_struct1_2_1
        self._r.is_struct1 = is_struct1_2
        is_struct2_1 = self._r.is_struct2
        ca(is_struct2_1["testval1"].mydat, [-4.489570e+13, 9.574895e-05, 4.081711e+06, 5.612839e-18, -1.078604e+05, 3.658139e+08, -4.748975e+05, -2.606481e+01, 3.016739e+15, 3.174709e+19, -4.572549e+17, 1.980389e-04, -3.551911e-10, 3.598401e-07, 2.659416e-12, -3.606157e+06, 2.059674e+17, -9.362336e-20, -3.299256e+17, -2.245745e+16])
        is_struct2_2 = {}
        is_struct2_2_1 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2",self._r)
        is_struct2_2_1.mydat = [6.931327e-21, 4.527137e-02, 1.260822e-18, 3.592805e-12, 1.088317e-05, 3.305865e+03, -9.798828e-20, 1.497504e+18, -3.653592e+01, 1.473952e+10, -1.003612e-20, 1.302159e+18, -8.544326e+05, 1.038521e+16, -2.845746e-18, -3.899909e-04, 4.785560e-02, -7.203365e-12, -1.500022e-14, -1.892753e-17]
        is_struct2_2["testval2"]= is_struct2_2_1
        self._r.is_struct2 = is_struct2_2
        ca(self._r.struct3.a1, [-8.483090e-19, -4.401548e-08, 3.908118e+00, 2.063513e-18, 4.237047e+18, -1.124681e-16, 3.924541e-01, -2.184335e-10, -1.978950e+11, 1.586365e+18, 1.712393e+00, -6.314723e+00, 1.196777e-16, -2.748704e-08, -1.289967e+02, -4.051137e+17, -1.902860e+10, -2.070486e+08, 3.622651e+06, 1.315398e+17])
        struct3_1 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService2.ostruct2",self._r)
        struct3_1.a1 = [-2.426765e+05, -9.410735e+01, -1.667915e+12, -4.084240e-05, 3.199460e+03, 8.256717e-12, -4.772119e-11, -1.061407e-13, 2.759750e+02, -1.212549e+10, 7.012690e+15, 3.953354e+04, -2.617985e-07, 1.104408e-21, -3.889366e+00, 4.549493e+16, -1.376791e+15, -3.445205e-21, 2.137830e-14, 4.620179e+18]
        self._r.struct3 = struct3_1


        #varvalue types (TODO: finish these...)

        ca(self._r.var_num.data, [-1680284833, -54562307, 732107275, 1470526962, -1389452949, 256801409, 261288152, 1728150828, 1322531658, -1640628174, 1036878614, 511108054, 2057847386, 288780916, 996595759])
        self._r.var_num = RobotRaconteurVarValue([-1046369769, 1950632347, 1140727074, -1277424443, 163999900, 970815027, 545593183, 514305170, 1896372264, 1385916382],"int32[]")
        if self._r.var_str.data != "Hello Client!":
            raise Exception()
        self._r.var_str = RobotRaconteurVarValue("Hello Server!","string")
        ca((self._r.var_struct.data).mydat, [-9.052731e+13, 4.151705e-17, -4.004463e+19, -2.838274e+03, 9.983314e+12, 2.764122e+10, -1.131486e+03, 2.418899e+12, 1.323675e-05, -4.602174e+13, 2.717530e+01, 1.193887e-10, -4.137578e+16, -1.246990e-19, 4.244315e-18, -2.833005e-08, 1.956266e-04, 4.130129e-21, 1.641708e-11, -4.488158e-19])
        var_struct_1 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2",self._r)
        var_struct_1.mydat = [-4.945426e-20, 1.763386e+13, 3.431578e-04, 4.411409e+17, -2.690201e+03, 3.025939e-10, -3.659846e+11, -4.780435e-10, -3.246816e+14, -1.815578e+04, 2.236455e+10, -4.639041e+14, 1.767930e+10, -1.636094e+05, -4.392462e-01, 2.225260e+04, -5.250245e+18, 8.755282e-12, 2.005819e-10, 2.702210e+04]
        self._r.var_struct = RobotRaconteurVarValue(var_struct_1,"RobotRaconteurTestService.teststruct2")
        if ((self._r.var_vector.data)[10]) != "Hello Client!":
            raise Exception()
        var_vector_1 = {}
        var_vector_1[11]= RobotRaconteurVarValue("Hello Server!","string")
        self._r.var_vector = RobotRaconteurVarValue(var_vector_1,"varvalue{int32}")
        if ((self._r.var_dictionary.data)["test1"]) != "Hello Client!":
            raise Exception()
        var_dictionary_1 = {}
        var_dictionary_1["test2"]= RobotRaconteurVarValue("Hello Server!","string")
        self._r.var_dictionary = RobotRaconteurVarValue(var_dictionary_1,"varvalue{string}")
        var_a_1 = self._r.var_multidimarray.data
        ca(var_a_1.Dims, [5, 4])
        ca(var_a_1.Real, [-4.915597e-01, 3.892823e+00, 2.622325e+08, -7.150935e+04, 9.418756e+00, 3.633879e+18, 3.522383e-03, -4.989811e+05, 2.027383e-03, -3.153241e+12, -6.948245e-21, -3.198577e+14, 6.172905e+09, 3.849430e+15, 8.600383e+13, 4.079437e-17, 3.194775e+06, 4.222550e-18, 1.758122e+17, -1.018308e+03])
        self._r.var_multidimarray = RobotRaconteurVarValue(MultiDimArray([5, 4], [3.792953e+00, 2.968121e-17, -3.976413e-15, 4.392986e+19, 2.197463e+10, -2.627743e-14, -2.184665e+17, 1.972257e-17, 9.929684e-03, -3.096821e+17, 3.598051e+11, -6.266015e-18, 1.811985e-11, 2.815232e-07, 7.469467e-06, 6.141798e+13, 3.105763e+09, -1.697809e-10, -4.141707e-17, 4.391634e+13]),"double[*]")


        #Test error passing
        err1 = False
        try:
            self._r.errtest = 1
        except Exception, e:
            err1 = True
        finally:
            pass
        if not err1:
            raise Exception()
        err2 = False
        try:
            d = self._r.errtest
        except Exception, e:
            err2 = True
        finally:
            pass
        if not err2:
            raise Exception()
        if self._r.nulltest != None:
            raise Exception()
        self._r.nulltest = None

    def TestFunctions(self):
        self._r.func1()
        self._r.func2(10, 20.34)
        if self._r.func3(2, 3.45) != 5.45:
            raise Exception()
        if self._r.meaning_of_life() != 42:
            raise Exception()
        errthrown = False
        try:
            self._r.func_errtest()
        except:
            errthrown = True
        finally:
            pass
        if not errthrown:
            raise Exception()

    def TestEvents(self):
        ev1=self._r.ev1
        ev1 += self.ev1_cb
        ev2=self._r.ev2
        ev2 += self.ev2_cb
        try:
            self._ev1_event = threading.Event()
            self._ev2_event = threading.Event()
            self._r.func1()
            self._r.func2(27.3, 98.23)
            if not self._ev1_event.wait(2):
                raise Exception()
            if not self._ev2_event.wait(2):
                raise Exception()
        finally:
            ev1=self._r.ev1
            ev1 -= self.ev1_cb
            ev2=self._r.ev2
            ev2 -= self.ev2_cb
            self._ev1_event = None
            self._ev2_event = None

    def ev1_cb(self):
        self._ev1_event.set()

    def ev2_cb(self, d, s):
        if d == 27.3 and s.mydat[0] == 98.23:
            self._ev2_event.set()

    def TestObjRefs(self):
        o1 = self._r.get_o1()
        o2_10 = self._r.get_o2(10)
        o2_34 = self._r.get_o2(34)
        o3_1 = self._r.get_o3(1)
        o4_myind = self._r.get_o4("myind")
        o4_specialind = self._r.get_o4("ind!@#$%^&*().<>     ")
        o2_10_o2_1_32 = o2_10.get_o2_2(32)
        o2_10_o2_1_32_o3_ind1 = o2_10_o2_1_32.get_o3_1("ind1")
        o2_10_o2_1_32_o3_ind2 = o2_10_o2_1_32.get_o3_1("ind2")
        o1.d1 = [-2.086627e+06, 3.092642e+04, -1.981667e+02, 1.963286e-20, 4.264052e-08, 3.594320e+12, -4.820517e-02, -3.629590e+06, 6.037089e-07, 3.328419e+06]
        o2_10.d1 = [4.978178e-14, 2.867603e-17, 4.471047e-21, -2.002902e+15, -2.910881e-03, -2.601092e-03, -3.043199e+16, -3.257109e-12, 1.834255e-11, -3.383015e+00]
        o2_34.d1 = [4.661927e-02, 2.334444e+02, 3.985567e+12, -2.324843e+01, -3.315866e+03, -4.442404e+10, 3.280626e-02, 2.334668e-12, -3.374202e-14, 4.809260e+02]
        o3_1.d1 = [-1.882441e-04, 2.065458e+14, -6.309214e-16, -3.181637e-07, -9.906616e+02, 1.684926e-14, 1.672252e+15, -3.950901e+01, -3.295950e-17, -3.080902e+13]
        o4_myind.d1 = [2.997950e-14, -1.077977e+17, 3.721399e-09, -1.289619e+18, 4.494844e+06, -4.918719e-15, 2.194759e+13, 2.554572e-09, 4.166299e-06, -1.409589e+04]
        o4_specialind.d1 = [3.404179e-08, -1.749189e-18, -3.219593e-09, 1.313794e+01, -4.193673e+10, -2.479829e+07, -2.617068e+04, 8.181730e+15, -2.003653e+18, -1.833401e+19]
        o2_10_o2_1_32.data = "Hello world!"
        o2_10_o2_1_32_o3_ind1.data2 = "Test string 1"
        o2_10_o2_1_32_o3_ind2.data2 = "Test string 2"
        self._r.o6_op(0)
        o6_1 = self._r.get_o6()
        o6_1_1 = o6_1.get_o2_1()
        o6_1.d1 = [0.0]
        o6_1_1.data = "Hello world!"
        self._r.o6_op(1)
        def f1():
            o6_1.d1=[0.0]
        def f2():
            o6_1_1.data="Hello world!"

        self.ShouldBeErr(f1)
        self.ShouldBeErr(f2)
        o6_2 = self._r.get_o6()
        o6_2.data = "Hello world!"
        self._r.o6_op(2)
        def f3():
            o6_2.data="Hello world!"
            self.ShouldBeErr(f3)
        o6_3 = self._r.get_o6()
        o6_3.add_val(2)


    def TestPipes(self):
        self._ee1 = threading.Event()
        self._ee2 = threading.Event()
        self._ee3 = threading.Event()
        e1 = self._r.p1.Connect(-1)
        e2 = self._r.p1.Connect(3432)
        e3 = self._r.p2.Connect(-1)
        e1.RequestPacketAck = True
        e1.PacketReceivedEvent += self.ee1_cb
        e1.PacketAckReceivedEvent += self.ee1_ack_cb
        e2.PacketReceivedEvent += self.ee2_cb
        e3.PacketReceivedEvent += self.ee3_cb
        self._packetnum = e1.SendPacket([1, 2, 3, 4])
        e1.SendPacket([5, 6, 7, 8])
        e1.SendPacket([-1, -2, -3, -5.32])
        e2.SendPacket([3.21])
        e2.SendPacket([4.72])
        e2.SendPacket([72.34])
        s1 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2",self._r)
        s1.mydat = [738.29]
        s2 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2",self._r)
        s2.mydat = [89.83]
        e3.SendPacket(s1)
        e3.SendPacket(s2)
        if not self._ee1.wait(5):
            raise Exception()
        if not self._ee2.wait(5):
            raise Exception()
        time.sleep(1)
        # if not self._ee3.wait(5):
        #    raise Exception()

        ca(e1.ReceivePacket(), [1, 2, 3, 4])
        ca(e1.ReceivePacket(), [5, 6, 7, 8])
        ca(e1.ReceivePacket(), [-1, -2, -3, -5.32])
        ca(e2.ReceivePacket(), [3.21])
        ca(e2.ReceivePacket(), [4.72])
        ca(e2.ReceivePacket(), [72.34])
        ca(e3.ReceivePacket().mydat, [738.29])
        ca(e3.ReceivePacket().mydat, [89.83])
        if not self._ack_recv:
            raise Exception()
        self._r.pipe_check_error()
        e1.Close()
        e2.Close()
        e3.Close()

    def ee1_cb(self, p):
        if p.Available < 3:
            return
        try:
            self._ee1.set()

        finally:
            pass

    def ee1_ack_cb(self, p, packetnum):

        if packetnum == self._packetnum:
            self._ack_recv = True

    def ee2_cb(self, p):
        if p.Available < 3:
            return
        try:
            self._ee2.set()

        finally:
            pass

    def ee3_cb(self, p):
        if p.Available < 2:
            return
        try:
            self._ee3.set()


        finally:
            pass

    def ShouldBeErr(self, a):
        err = False

        try:
            a()
        except:
            err = True
        finally:
            pass
        if not err:
            raise Exception()

    def TestCallbacks(self):
        self._cb1_called = False
        self._cb2_called = False
        self._cb3_called = False
        self._cb4_called = False
        self._cb5_called = False
        self._r.cb1.Function = self.cb1_func
        self._r.cb2.Function = self.cb2_func
        self._r.cb3.Function = self.cb3_func
        self._r.cb_meaning_of_life.Function = self.cb_meaning_of_life_func
        self._r.cb_errtest.Function = self.cb_errtest
        self._r.test_callbacks()
        if not self._cb1_called or not self._cb2_called or not self._cb3_called or not self._cb4_called or not self._cb5_called:
            raise Exception()

    def cb1_func(self):
        self._cb1_called = True

    def cb2_func(self, d1, d2):
        if d1 != 739.2 or d2 != 0.392:
            raise Exception()
        self._cb2_called = True

    def cb3_func(self, d1, d2):
        self._cb3_called = True
        return d1 + d2 + 3.14

    def cb_meaning_of_life_func(self):
        self._cb4_called = True
        return 42

    def cb_errtest(self):
        self._cb5_called = True
        raise Exception("This is a test")

    def TestWires(self):
        self._w1_called = False
        self._w2_called = False
        self._w3_called = False
        w1 = self._r.w1.Connect()
        w2 = self._r.w2.Connect()
        w3 = self._r.w3.Connect()
        w11=w1.WireValueChanged; w11 += self.w1_changed
        w21=w2.WireValueChanged; w21 += self.w2_changed
        w31=w3.WireValueChanged; w31 += self.w3_changed
        w1.OutValue = [0]
        s1 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2",self._r)
        s1.mydat = [0]
        w2.OutValue = s1
        a1 = MultiDimArray([1, 1], [0])
        w3.OutValue = a1
        w1.OutValue = [-2.377683e+02, -6.760080e-08, 4.191315e-18, -4.621977e+07, -1.570323e+03, -4.163378e+03, -2.506701e+13, -4.755701e+18, -1.972380e-19, 1.791593e-11]
        s2 = RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2",self._r)
        s2.mydat = [-1.014645e-21, 4.743740e+11, 5.804886e-04, 2.963852e-20, 4.277621e-21, -1.168151e+13, -2.638708e-18, -5.123312e+14, 1.261123e-05, 2.552626e-10]
        w2.OutValue = s2
        a2 = MultiDimArray([2, 5], [2058500854, -611248192, 197490486, -517717939, -513450368, 296469979, 645365194, 2043654604, -1672941174, 710030901])
        w3.OutValue = a2
        time.sleep(.5)
        in1 = w1.InValue
        ca(in1, [-2.377683e+02, -6.760080e-08, 4.191315e-18, -4.621977e+07, -1.570323e+03, -4.163378e+03, -2.506701e+13, -4.755701e+18, -1.972380e-19, 1.791593e-11])
        in2 = w2.InValue
        ca(in2.mydat, [-1.014645e-21, 4.743740e+11, 5.804886e-04, 2.963852e-20, 4.277621e-21, -1.168151e+13, -2.638708e-18, -5.123312e+14, 1.261123e-05, 2.552626e-10])
        in3 = w3.InValue
        ca(in3.Dims, [2, 5])
        ca(in3.Real, [2058500854, -611248192, 197490486, -517717939, -513450368, 296469979, 645365194, 2043654604, -1672941174, 710030901])
        if not self._w1_called or not self._w2_called or not self._w3_called:
            raise Exception()

    def w1_changed(self, c, value, t):
        self._w1_called = True

    def w2_changed(self, c, value, t):
        self._w2_called = True

    def w3_changed(self, c, value, t):
        self._w3_called = True

    def TestMemories(self):
        self.test_m1()
        self.test_m2()
        self.test_m3()

    def test_m1(self):
        if self._r.m1.Length != 100:
            raise Exception()
        m1_1 = numpy.array([0]*11,numpy.float64)
        self._r.m1.Read(10, m1_1, 1, 10)
        ca(m1_1, [0, -1.478723e-16, 1.507042e-05, -2.046271e+13, 4.014775e+06, 4.140740e+10, 1.318907e+16, -2.312403e+17, 4.463696e-13, 9.173421e-04, 6.169183e-21])
        m1_2 = numpy.array([3.462892e+10, -1.149841e-18, 4.649317e-15, -3.632280e-19, -5.252280e+07, 1.800453e-07, 3.772468e-04, -1.911891e+09, -3.018967e-14, 4.835062e-06, 5.269663e+13, 4.946221e+03],numpy.float64)
        self._r.m1.Write(20, m1_2, 2, 8)
        m1_3 = numpy.array([0]*100,numpy.float64)
        self._r.m1.Read(0, m1_3, 0, 100)
        m1_4 = numpy.array([-2.675014e-13, 6.884672e-07, 4.855899e-02, 1.634267e-08, -5.346105e+06, 9.245749e+09, 2.174639e+16, -3.574166e+04, 3.063678e+16, 4.748279e-16, -1.478723e-16, 1.507042e-05, -2.046271e+13, 4.014775e+06, 4.140740e+10, 1.318907e+16, -2.312403e+17, 4.463696e-13, 9.173421e-04, 6.169183e-21, 3.643045e+09, -3.784476e+13, -1.878617e-21, -4.122785e+01, -2.477761e+15, -5.220540e-11, -3.930894e-19, 3.980082e-12, -3.681569e-20, 4.675366e+19, -7.454667e-06, -1.529932e+17, -3.707663e-04, -3.356188e-20, -2.393304e-07, 1.339372e-18, -3.735916e-15, 1.715447e+01, 1.316085e+02, 9.603036e-05, 1.458992e+16, 9.228113e+11, 1.099841e-12, -2.484793e-09, 4.826956e-19, -3.662630e-11, -3.274562e+10, 1.866042e-12, 4.061219e-13, 1.307997e-18, -1.210979e+08, 4.036328e+02, -2.713849e-11, -3.673995e-01, -4.576021e+03, 1.519751e+03, 1.792427e-16, -2.033399e+18, 4.341947e+08, -1.699292e-09, -1.007978e-21, 3.200139e-15, -3.157557e+03, -3.717883e-15, 4.337614e+02, -3.666534e-12, -1.821013e-14, -2.260577e-20, 1.722045e-06, 1.886614e+00, -1.278609e+15, 2.923499e-03, 4.969081e+02, 4.438380e-06, -3.890489e-11, -3.261564e-17, 6.172945e-10, 4.951740e+19, 3.460327e+11, -3.600349e-16, 2.419445e+11, -9.124824e+10, 4.127522e+04, 1.443468e+00, -3.968841e-21, -2.507203e+05, 2.214239e+13, -3.327687e+07, 1.167160e+09, -4.361249e-11, -4.609514e+14, -2.461408e+13, 5.584758e+06, 3.989706e-07, 2.597151e-12, -2.961640e+08, -2.173964e-02, -1.866864e-11, 4.832786e-08, 2.713705e-07],numpy.float64)
        #Array.Copy(m1_2, 2, m1_4, 20, 8)
        m1_4[20:(20+8)]=m1_2[2:(2+8)]
        ca(m1_3, m1_4)

    def test_m2(self):
        if not self._r.m2.Complex:
            raise Exception()
        print self._r.m2.DimCount
        if self._r.m2.DimCount != 5:
            raise Exception()
        m2_dims = self._r.m2.Dimensions
        ca(m2_dims, [10, 10, 10, 10, 10])
        m1 = MultiDimArrayToNumPy(MultiDimArrayTest.LoadDoubleArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray1.bin")),numpy.complex128)
        m2 = MultiDimArrayToNumPy(MultiDimArrayTest.LoadDoubleArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray2.bin")),numpy.complex128)
        m3 = MultiDimArrayToNumPy(MultiDimArrayTest.LoadDoubleArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray3.bin")),numpy.complex128)
        m4 = MultiDimArrayToNumPy(MultiDimArrayTest.LoadDoubleArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray4.bin")),numpy.complex128)
        m5 = MultiDimArrayToNumPy(MultiDimArrayTest.LoadDoubleArrayFromFile(path.join(MultiDimArrayTest.TestDataPath,"testmdarray5.bin")),numpy.complex128)
        self._r.m2.Write([0, 0, 0, 0, 0], m1, [0, 0, 0, 0, 0], m1.shape)
        m1_2 = numpy.zeros([10, 10, 10, 10, 10],numpy.complex128)
        self._r.m2.Read([0, 0, 0, 0, 0], m1_2, [0, 0, 0, 0, 0], m1.shape)
        numpy.array_equal(m1, m1_2)
        self._r.m2.Write([2, 2, 3, 3, 4], m2, [0, 2, 0, 0, 0], [1, 5, 5, 2, 1])
        m2_2 = numpy.zeros([10, 10, 10, 10, 10],numpy.complex128)
        self._r.m2.Read([0, 0, 0, 0, 0], m2_2, [0, 0, 0, 0, 0], m1.shape)

        m6 = numpy.zeros([2, 2, 1, 1, 10], numpy.complex128)
        self._r.m2.Read([4, 2, 2, 8, 0], m6, [0, 0, 0, 0, 0], [2, 2, 1, 1, 10])
        numpy.array_equal(m4,m6)

        m7 = numpy.zeros([4, 4, 4, 4, 10],numpy.complex128)
        self._r.m2.Read([4, 2, 2, 8, 0], m7, [2, 1, 2, 1, 0], [2, 2, 1, 1, 10])
        numpy.array_equal(m5,m7)



    def test_m3(self):
        m1 = MultiDimArrayToNumPy(MultiDimArrayTest.LoadByteArrayFromFile(path.join(MultiDimArrayTest.TestDataPath, "testmdarray_b1.bin")),numpy.uint8)
        m2 = MultiDimArrayToNumPy(MultiDimArrayTest.LoadByteArrayFromFile(path.join(MultiDimArrayTest.TestDataPath, "testmdarray_b2.bin")),numpy.uint8)
        m3 = MultiDimArrayToNumPy(MultiDimArrayTest.LoadByteArrayFromFile(path.join(MultiDimArrayTest.TestDataPath, "testmdarray_b3.bin")),numpy.uint8)
        m4 = MultiDimArrayToNumPy(MultiDimArrayTest.LoadByteArrayFromFile(path.join(MultiDimArrayTest.TestDataPath, "testmdarray_b4.bin")),numpy.uint8)
        m5 = MultiDimArrayToNumPy(MultiDimArrayTest.LoadByteArrayFromFile(path.join(MultiDimArrayTest.TestDataPath, "testmdarray_b5.bin")),numpy.uint8)
        self._r.m3.Write([0, 0], m1, [0, 0], [1024, 1024])
        m1_2 = numpy.zeros([1024, 1024],numpy.uint8)
        self._r.m3.Read([0, 0], m1_2, [0, 0], [1024, 1024])
        numpy.array_equal(m1,m1_2)

        self._r.m3.Write([50, 100], m2, [20, 25], [200, 200])
        m2_2 = numpy.zeros([1024, 1024], numpy.uint8)
        self._r.m3.Read([0, 0], m2_2, [0, 0], [1024, 1024])
        numpy.array_equal(m2,m2_2)
        m6 = numpy.zeros([200, 200], numpy.uint8)
        self._r.m3.Read([65, 800], m6, [0, 0], [200, 200])
        numpy.array_equal(m4,m6)

        m7 = numpy.zeros([512, 512], numpy.uint8)
        self._r.m3.Read([65, 800], m7, [100, 230], [200, 200])
        numpy.array_equal(m5,m7)


    def TestAuthentication(self, url):
        #Test two different logins

        cred1={"password": RobotRaconteurVarValue("testpass1","string")}
        r1 = RobotRaconteurNode.s.ConnectService(url, "testuser1", cred1)
        r1.func3(2.2, 3.3)
        RobotRaconteurNode.s.DisconnectService(r1)

        cred2={"password": RobotRaconteurVarValue("testpass2","string")}
        r2 = RobotRaconteurNode.s.ConnectService(url, "testuser2", cred2)
        r2.func3(2.2, 3.3)
        RobotRaconteurNode.s.DisconnectService(r2)
        #Check an invalid password
        err = False
        r3 = None
        try:
            r3 = RobotRaconteurNode.s.ConnectService(url, "testuser2", cred1)
            r3.func3(2.2, 3.3)
        except Exception, e:
            err = True
            try:
                if (r3 != None):
                    RobotRaconteurNode.s.DisconnectService(r3)

            finally:
                pass
        finally:
            pass
        if not err:
            raise Exception()
        err2 = False
        #Check no password
        r4 = None
        try:
            r4 = RobotRaconteurNode.s.ConnectService(url)
            r4.func3(2.2, 3.3)
        except Exception, e:
            err2 = True
            try:
                RobotRaconteurNode.s.DisconnectService(r4)

            finally:
                pass
        finally:
            pass
        if not err2:
            raise Exception()

    def TestObjectLock(self, url):
        #Run a test, check 6 things:
        #1. Exclusive username lock works as expected (user with lock can acces, other user can't)
        #2. Check that session-level lock works as expected (only one session can access the locked object)
        #3. Check that "sub-tree" objects lock as expected
        #5. Object lock release works
        #6. Object lock override works
        #Log in twice

        cred1={"password": RobotRaconteurVarValue("testpass1","string")}
        r1 = RobotRaconteurNode.s.ConnectService(url, "testuser1", cred1)
        #Log in again with "testuser1" username

        cred2={"password": RobotRaconteurVarValue("testpass2","string")}
        r2 = RobotRaconteurNode.s.ConnectService(url, "testuser1", cred1)
        r1_o = r1.get_o1()
        r1_o_o2 = r1_o.get_o2_1()
        r2_o = r2.get_o1()
        r2_o_o2 = r2_o.get_o2_1()
        r3 = RobotRaconteurNode.s.ConnectService(url, "testuser2", cred2)
        r3_o = r3.get_o1()
        r3_o_o2 = r3_o.get_o2_1()
        #Make sure all the objects work
        r1.func3(2.2, 3.3)
        r1_o.d1 = [1.0]
        print "Here"
        r1_o_o2.data = "Hello world"
        r2.func3(2.2, 3.3)
        r2_o.d1 = [1.0]
        r2_o_o2.data = "Hello world"
        r3.func3(2.2, 3.3)
        r3_o.d1 = [1.0]
        r3_o_o2.data = "Hello world"
        #Lock the object by username
        RobotRaconteurNode.s.RequestObjectLock(r1_o, RobotRaconteurObjectLockFlags_USER_LOCK)
        print "Locked"
        #Check that all users that should access the objects can
        r1.func3(2.2, 3.3)
        r1_o.d1 = [1.0]
        r1_o_o2.data = "Hello world"
        r2.func3(2.2, 3.3)
        r2_o.d1 = [1.0]
        r2_o_o2.data = "Hello world"
        r3.func3(2.2, 3.3)
        #Check that objects that shouldn't be able to access the objects can't

        def f1():
            r3_o.d1=[1.0]
        def f2():
            r3_o_o2.data="Hello world"


        self.ShouldBeErr(f1)
        self.ShouldBeErr(f2)
        #Unlock and recheck all
        RobotRaconteurNode.s.ReleaseObjectLock(r1_o)
        r1.func3(2.2, 3.3)
        r1_o.d1 = [1.0]
        r1_o_o2.data = "Hello world"
        r2.func3(2.2, 3.3)
        r2_o.d1 = [1.0]
        r2_o_o2.data = "Hello world"
        r3.func3(2.2, 3.3)
        r3_o.d1 = [1.0]
        r3_o_o2.data = "Hello world"
        #Relock, test that the lock is active, and then close the connection.  The lock should release.  The
        #second session is closed first, and should not release the lock.
        RobotRaconteurNode.s.RequestObjectLock(r1_o, RobotRaconteurObjectLockFlags_USER_LOCK)
        def f3():
            r3_o.d1=[1.0]
        self.ShouldBeErr(f3)
        r2_o.d1 = [1.0]
        RobotRaconteurNode.s.DisconnectService(r2)
        #Object still should be locked

        def f4():
            r3_o.d1=[1.0]
        self.ShouldBeErr(f4)
        #Now close the session and lock should be released
        RobotRaconteurNode.s.DisconnectService(r1)
        r3_o.d1 = [1.0]
        #Reconnect the first two test sessions
        r1 = RobotRaconteurNode.s.ConnectService(url, "testuser1", cred1)
        r2 = RobotRaconteurNode.s.ConnectService(url, "testuser2", cred2)
        r1_o = r1.get_o1()
        r1_o_o2 = r1_o.get_o2_1()
        r2_o = r2.get_o1()
        r2_o_o2 = r2_o.get_o2_1()
        #Test the exclusive client lock
        RobotRaconteurNode.s.RequestObjectLock(r1_o, RobotRaconteurObjectLockFlags_CLIENT_LOCK)
        r1_o.d1 = [1.0]
        def f5():
            r2_o.d1=[1.0]
        self.ShouldBeErr(f5)
        def f6():
            r3_o.d1=[1.0]
        self.ShouldBeErr(f6)
        #Test the lock override by testsuperpass

        cred5={"password": RobotRaconteurVarValue("superpass1","string")}
        r5 = RobotRaconteurNode.s.ConnectService(url, "testsuperuser", cred5)
        r5_o = r5.get_o1()
        RobotRaconteurNode.s.ReleaseObjectLock(r5_o)
        #Make sure the lock is released
        r2_o.d1 = [1.0]
        r3_o.d1 = [1.0]
        #Close all connections
        RobotRaconteurNode.s.DisconnectService(r1)
        RobotRaconteurNode.s.DisconnectService(r2)
        RobotRaconteurNode.s.DisconnectService(r3)
        RobotRaconteurNode.s.DisconnectService(r5)

    def TestMonitorLock(self, url):
        #The monitor lock aquires an exclusive sock to a single thread on the client.
        #This lock is for a single thread, and works for all clients and the service if
        #it is checking for monitor locks.
        r1 = RobotRaconteurNode.s.ConnectService(url)
        r2 = RobotRaconteurNode.s.ConnectService(url)
        r1_o = r1.get_o1()
        r1_o_o2 = r1_o.get_o2_1()
        r2_o = r2.get_o1()
        r2_o_o2 = r2_o.get_o2_1()
        #Make sure everything works
        r1.func3(2.2, 3.3)
        r1_o.d1 = [1.0]
        r1_o_o2.data = "Hello world"
        r2.func3(2.2, 3.3)
        r2_o.d1 = [1.0]
        r2_o_o2.data = "Hello world"
        #Make sure that locks work as expected
        t1 = False
        t2 = False
        e1 = threading.Event()
        #AutoResetEvent e2 = new AutoResetEvent(false);
        threaderr = False
        def f1():
            try:
                r2.func3=(2.2,3.3)
                r2_o_o2.data="Hello world"

                e1.set()
                RobotRaconteurNode.s.MonitorEnter(r2_o)
                if (t1): raise Exception()
                t2=True

                r2_o.d1=[0.0]
                RobotRaconteurNode.s.MonitorExit(r2_o)
            except:
                import traceback
                traceback.print_exc()
                threaderr=True



        t = threading.Thread(None,f1)
        #ShouldBeErr<ObjectLockedException>(delegate() { r2_o.d1 = new double[] { 0.0 }; });
        RobotRaconteurNode.s.MonitorEnter(r1_o)
        t.start()
        t1 = True

        time.sleep(0.01)
        r1.func3(2.2, 3.3)
        r1_o.d1 = [0.0]
        if t2:
            raise Exception()
        t1 = False
        RobotRaconteurNode.s.MonitorExit(r1_o)
        t.join()
        if threaderr:
            raise Exception()

class testroot_impl(object):

    def __init__(self):
        self._o1=sub1_impl()
        self._o2={}
        self._o2_lock=threading.RLock()
        self._o3={}
        self._o3_lock=threading.RLock()
        self._o4={}
        self._o4_lock=threading.RLock()
        self._o5=sub1_impl()
        self._o6=sub1_impl()

        self._packet_sent=False
        self._p1_lock=threading.RLock()
        self._ack_recv=False
        self._p1=None

        self._p2=None
        self._p2_lock=threading.RLock()

        self.ev1=EventHook()
        self.ev2=EventHook()
        self.ev3=EventHook()

        mdat1=numpy.array([-2.675014e-13, 6.884672e-07, 4.855899e-02, 1.634267e-08, -5.346105e+06, 9.245749e+09, 2.174639e+16, -3.574166e+04, 3.063678e+16, 4.748279e-16, -1.478723e-16, 1.507042e-05, -2.046271e+13, 4.014775e+06, 4.140740e+10, 1.318907e+16, -2.312403e+17, 4.463696e-13, 9.173421e-04, 6.169183e-21, 3.643045e+09, -3.784476e+13, -1.878617e-21, -4.122785e+01, -2.477761e+15, -5.220540e-11, -3.930894e-19, 3.980082e-12, -3.681569e-20, 4.675366e+19, -7.454667e-06, -1.529932e+17, -3.707663e-04, -3.356188e-20, -2.393304e-07, 1.339372e-18, -3.735916e-15, 1.715447e+01, 1.316085e+02, 9.603036e-05, 1.458992e+16, 9.228113e+11, 1.099841e-12, -2.484793e-09, 4.826956e-19, -3.662630e-11, -3.274562e+10, 1.866042e-12, 4.061219e-13, 1.307997e-18, -1.210979e+08, 4.036328e+02, -2.713849e-11, -3.673995e-01, -4.576021e+03, 1.519751e+03, 1.792427e-16, -2.033399e+18, 4.341947e+08, -1.699292e-09, -1.007978e-21, 3.200139e-15, -3.157557e+03, -3.717883e-15, 4.337614e+02, -3.666534e-12, -1.821013e-14, -2.260577e-20, 1.722045e-06, 1.886614e+00, -1.278609e+15, 2.923499e-03, 4.969081e+02, 4.438380e-06, -3.890489e-11, -3.261564e-17, 6.172945e-10, 4.951740e+19, 3.460327e+11, -3.600349e-16, 2.419445e+11, -9.124824e+10, 4.127522e+04, 1.443468e+00, -3.968841e-21, -2.507203e+05, 2.214239e+13, -3.327687e+07, 1.167160e+09, -4.361249e-11, -4.609514e+14, -2.461408e+13, 5.584758e+06, 3.989706e-07, 2.597151e-12, -2.961640e+08, -2.173964e-02, -1.866864e-11, 4.832786e-08, 2.713705e-07 ],numpy.float64)
        self.m1=ArrayMemory(mdat1)
        self.m2=MultiDimArrayMemory(numpy.zeros([10, 10, 10, 10, 10],numpy.complex128))
        self.m3=MultiDimArrayMemory(numpy.zeros([1024,1024],numpy.uint8))


    @property
    def d1(self):
        return 12.345

    @d1.setter
    def d1(self,value):
        if (value!=3.456):
            raise Exception()

    @property
    def d2(self):
        return [1.374233e+19, 2.424327e-04, -1.615609e-02, 3.342963e-21, -4.308134e+14, -1.783430e-07, 2.214302e+18, -1.091018e+17, 3.279396e-20, 2.454183e-01, 1.459922e+07, -3.494941e+16, -7.949200e-21, 1.720101e+17, -1.041015e+16, 1.453541e+05, 1.125846e+06, 1.894394e+07, 1.153038e-17, -3.283589e+06, 2.253268e-10, -3.897051e+06, 1.362011e+05, 5.501697e-19, -4.854610e+01, -1.582705e-05, 7.622313e+04, 2.104642e+08, -1.294512e-06, -1.426230e-19, -4.319619e-15, 9.837716e+03, -4.949316e-01, -2.173576e+02, 2.730509e-19, -2.123803e+05, 1.652596e-17, -2.066863e-09, 3.856560e-08, 1.379652e+18, -2.119906e+16, 4.860679e-05, -1.681801e-10, -1.569650e-15, 3.984306e-21, 3.283336e+08, -9.222510e-16, -3.579521e-02, 1.279363e-05, 3.920153e-12, 4.737275e-15, -4.427587e+06, -3.826670e-14, 2.492484e-04, 4.996082e+09, 4.643228e-11, 2.809952e-17, -2.224883e-13, -4.442602e+18, 4.422736e+11, 4.969282e-18, 4.937908e-15, 6.973867e-22, 1.908796e-19, 4.812115e-08, 1.753516e-02, -3.684764e+02, 1.557482e-17, -1.176997e-11, 1.772798e-05, 4.877622e-16, 1.107926e+11, 4.097985e-14, 2.714049e-18, 3.198732e+15, -1.052497e-01, -5.003982e+07, -1.538353e-04, 3.045308e+17, 1.176208e-18, 1.268710e-10, -1.269719e-05, -2.989599e+00, -3.721343e-11, -1.444196e-10, -2.030635e+04, 2.070258e+16, -3.001278e-14, 1.116018e+14, 4.999239e+15, 4.286177e-21, -2.972550e+10, 3.549075e-20, -2.874186e-06, 2.994430e+09, 2.978356e+10, -2.364977e+07, 2.807278e-01, -3.279567e-10, 4.567428e+05, 1.612242e+07, 4.102315e+05, -1.069501e-20, 2.887812e+10, 4.384194e-09, -2.936771e-11, -4.164448e+07, 3.391389e+04, -3.923673e+17, -2.735518e-22, -2.019257e-01, 3.014806e+15, -3.885050e-15, -2.806241e-20, 3.077066e+18, -1.574438e+14, -3.131588e+19, 4.812541e+03, 4.435881e+16, -3.843380e+02, -7.522165e+03, -3.668055e-21, 2.603478e-08, 2.928775e+08, 2.892123e+00, -1.594119e+04, -4.817379e-01, -2.121948e+03, -8.872132e-09, -3.909318e-06, -3.849648e-14, -4.554589e+18, 4.410297e-15, -2.976295e-04, -2.298802e+10, 4.981337e-07, 5.364781e-12, 1.536953e+07, -4.082889e-07, 1.670759e-21, 4.009147e-13, -4.691543e-18, -2.597887e-13, 2.368696e+18, -2.585884e-07, -5.209726e-03, -2.568300e+06, 2.184692e-20, -1.799204e+16, 1.397292e+04, 4.277966e+13, -4.072388e+09, -2.324749e+16, -4.717399e+10, -2.853124e-05, -3.664750e+11, -3.864796e-08, 3.265198e+07, -3.309827e+19, 3.222296e+03, 2.366113e-19, -3.425143e+14, 1.627821e-08, 4.987622e+00, -1.402489e-17, -1.303904e+15, -2.042850e+17, -1.399340e+09, -3.560871e+05, -4.251240e-21, -7.806581e-10, 1.723498e+00, -2.030115e+08, 4.595621e-19, 1.174387e-10, 3.474174e+14, -4.159866e+03, -1.833464e-19, -3.650925e+05, 3.757361e-03, -1.854280e-10, -1.856982e-13, 1.685338e+08, 4.051670e-11, 4.095232e+03, -2.956025e-16, 4.986423e-05, 4.941458e+10, 4.145946e+11, 3.402975e+14, -1.954363e+11, -2.274907e+10, -3.162121e-17, -5.027950e-07, 4.135173e-02, -3.777913e-04, -4.898637e+15, 2.354747e-02, -6.884549e+13, -1.896920e-05, -1.914414e+15, -1.196744e-19, -4.692974e-01, 8.586675e-10, -2.204766e-17, -3.586447e-14, 1.751276e+17, -2.546189e-05, -2.248796e+03, -9.445830e+02, 1.150138e+03, 4.586691e+11, -2.582686e-15, -2.795788e+12, -3.409768e+07, -2.172186e-03, -1.457882e+06, -4.153022e+13, -4.255977e-08, 3.216237e-07, 4.935803e+02, -4.248965e-16, 1.740357e+07, 4.635370e+19, -4.099930e-14, 2.758885e-16, -4.714106e-05, -4.556226e-20, -4.290894e-19, 1.174284e-09, -1.443257e+16, -2.279471e-08, -3.030819e-16, 1.535128e+18, -3.248271e-07, 3.079855e-21, -3.056403e-02, -1.368113e-12, 4.004190e-10, 4.955150e+07, -2.494283e-16, 2.186037e+05, -1.232946e+03, 5.586112e-05, -2.288144e+17, 2.515602e-19, -4.064132e+08, -3.217400e-02, -2.620215e+07, 2.283421e-14, -1.130075e+08, 3.304955e-03, 1.352402e+01, 6.255755e-03, -3.913649e-08, 5.474984e+01, -4.712294e-08, 3.548418e-16, 1.276896e+12, 2.007320e-08, 3.025617e+04, -2.544836e+14, -2.087825e+17, -3.285556e-09, 2.605304e+07, -1.876210e+07, 3.734943e-10, -3.862726e-15, -4.227362e-05, 1.267773e+14, -1.706991e-05, 3.737441e+10, 2.641527e+01, 4.439891e+10, -1.444933e-05, -2.190034e-12, 8.059924e-18, -1.324313e+18, -1.420214e-10, 3.940158e-20, 3.943349e-02, -2.685925e+19, 4.334133e-05, 3.171371e-21, 2.094486e+12, 1.331741e+03, 1.205892e-02, 1.791416e+04, 3.899239e+10, 6.581991e+06, -3.860368e+11, -3.853916e-02, 1.314566e+09, 3.923126e+03, -3.509905e+13, -4.332430e+06, -1.713419e+01, -1.244104e-14, -5.529613e+01, 6.630349e+06, 1.053668e+10, 3.312332e-05, -1.252220e+08, 3.997107e-07, 1.847068e-13, -2.393157e-11, -2.083719e-10, -4.927155e+11, 2.666499e-15, 4.087292e-10, 4.082567e-10, -2.017655e+07, 9.108015e+15, -4.199693e-15, -4.969705e-17, 1.769881e-02, 1.745504e+00, 2.200377e-16, -4.404838e-06, -1.317122e-15, 7.210560e+08, 1.282439e-18, -3.204957e-06, -1.624277e+05, 4.570975e-22, 1.261776e+04, 4.416193e+12, -4.343457e-18, 4.095420e-14, 4.951026e-09, 2.261753e-15, 4.125062e+05, -4.448849e+11, -3.184924e+06, -2.050956e+05, -9.895539e+09, 4.541548e+11, -4.230580e+11, -4.268059e-15, -4.393836e+09, -2.514832e-08, 3.322394e-04, 2.597384e-18, 1.316619e-11, -2.250081e+16, 2.179579e-10, -1.838295e+04, -1.995626e-17, -4.656110e+17, 3.481814e-07, -2.859273e-11, -2.011768e-06, -1.809342e-17, -3.242126e+10, -1.873723e+08, -2.833009e-12, -3.758282e+12, 2.970198e+15, -2.667738e-01, -3.689173e+11, 1.008362e-10, -1.526867e-20, -1.439753e+06, -6.154602e+16, 4.165816e+00, -1.597823e-09, -1.862803e+14, -2.222766e+15, -2.892587e+17, -4.230426e-14, 2.999121e-21, 1.642245e+00, 1.590694e-14, -4.469755e-06, 2.700655e+12, -1.822443e-02, -4.889338e-16, -3.174990e-11, 4.146024e-03, 1.313280e+01, 3.235142e+15, 3.500547e+00, -4.413708e+03, 1.485548e+16, -1.660821e-11, -4.334510e-22, -1.209739e+04, 1.149570e+12, -4.537849e+00, -3.628402e-16, 2.748853e-12, -4.818907e-21]
    @d2.setter
    def d2(self,value):
        ca(value,[8.805544e-12, 3.735066e+12, 3.491919e+17, 4.979833e+12, -4.042302e+00, 2.927731e-12, 5.945355e+11, -3.965351e+06, 4.866934e-14, 1.314597e+04, -2.059923e-11, -5.447989e-20, 1.267732e-21, -2.603983e+10, 2.417961e+03, 3.515469e-16, 1.731329e-01, -2.854408e-04, 2.908090e-06, 3.354746e+08, 9.405914e+05, -3.665276e-01, -2.036897e+02, 3.489765e-01, -3.207702e+11, -2.105708e+18, -1.485891e+13, -7.059704e+04, 3.528381e+11, 4.586056e+02, -8.107050e-16, -1.007106e+09, 2.964453e+05, -3.628810e+05, -2.816870e-14, 5.665387e+09, 8.518736e+11, -1.179981e+12, -1.506569e-21, 1.113076e-06, -4.782847e+06, 8.906463e+17, 2.729604e+03, -3.430604e+16, 2.626956e-07, 1.543395e+15, 3.407777e-21, 1.231519e+06, -4.808410e+16, 2.649811e+10, 2.546524e+01, -3.533472e-13, -3.732759e+04, 1.951505e-20, 9.338953e-21, -1.627672e-04, 1.807084e-19, -4.489206e-17, -2.654284e+08, -2.136947e+16, -3.690031e+09, 3.372245e-14, 4.946361e-11, -1.330965e-01, 2.479789e-17, 2.750331e-18, -4.301452e-03, 3.895091e+19, 2.515863e+13, 6.879298e+12, -2.925884e-15, -2.826248e+00, -4.864526e-06, 2.614765e+00, 4.488816e-19, 2.231337e+15, -7.004595e+07, 2.506835e-08, -2.187450e-02, -2.220025e-07, 1.688346e+02, 8.125250e-07, -4.819391e+10, -1.643306e-14, -4.768222e-18, -4.472162e-16, 2.487563e-01, -3.924904e-15, -1.186331e+06, 2.397369e+01, -3.137448e-02, 1.016507e+06, 2.584749e-16, 8.212180e-08, 1.631561e-12, -4.927066e-08, 1.448920e-14, -4.371505e+03, 2.050871e-21, 2.523287e+01, 7.778552e-05, -4.437786e+18, -1.118552e-07, -3.543717e-09, -5.327587e-07, -1.083197e-17, 2.578295e-10, -4.952430e-12, -3.008597e-13, 3.010829e+01, -6.109332e+09, -2.428341e-03, 9.399191e-01, -4.827230e-06, 1.013860e+10, -2.870341e-20, 4.281756e+11, 1.043519e-09, 2.378027e+06, 2.605309e+09, -4.939600e-04, -2.193966e+08, 4.022755e-03, 2.668705e-09, -1.087393e-18, 1.927676e-12, -1.694835e+10, 3.554035e-03, -1.299796e+01, -1.692862e+07, 2.818156e+07, -2.606821e-13, 1.629588e-15, -7.069991e-16, 1.205863e-19, 2.491209e-17, -3.757951e+04, 3.110266e-04, -4.339472e+11, -3.172428e+02, 1.579905e+09, 2.859499e-01, 4.241852e-06, 2.043341e-09, 2.922865e-16, -2.580974e+01, -3.147566e-02, 1.160590e+03, -2.238096e+01, -1.984601e-13, 2.636096e-03, 8.422872e-04, 2.026040e-16, -3.822500e+01, -2.190513e-18, 3.229839e-11, -2.958164e+06, -8.354021e+11, 3.625367e+08, -4.558085e-01, 1.274325e+04, -2.492750e+05, 3.739269e+18, -3.985407e-03, 3.575816e-13, 1.376847e+06, -6.682659e-20, -9.200014e+08, -2.278973e+10, -3.555184e-04, 3.821512e-10, 5.944167e+07, -2.576511e-15, 1.232459e+02, -3.187831e+02, -4.882568e+12, -1.670486e+05, -2.339878e-20, -4.985496e-16, -2.937093e+17, 8.981723e-06, -5.460686e-04, 1.090528e-11, -4.321598e+17, -3.577227e-08, 2.880194e+01, -4.277921e+00, -4.145678e-02, 4.930810e+08, -4.525745e-21, 4.648764e+07, -2.564920e+16, 1.075546e+01, 3.777591e-18, 1.419816e-08, 1.419490e+10, 1.479453e-19, -4.933130e+13, 4.580471e+15, -3.160785e+02, -2.885209e+06, 2.384424e-03, 1.030777e-12, 2.652784e+04, 4.435144e+10, 3.102484e+17, 4.725294e+11, -3.817788e-04, 4.074841e-01, -7.248042e-13, -4.502531e-08, 2.203521e+01, -4.457124e+01, -2.961745e+06, -3.237080e+14, -3.482497e-19, 1.534088e+05, 4.759060e-14, 2.333791e+04, -4.002051e-03, 3.278553e-06, -2.307217e+13, -2.999411e+19, -9.804484e+02, -1.793367e+01, 3.111735e+07, -4.457329e+10, -2.067659e-13, -5.927573e+03, 6.979879e+10, 3.556110e-06, -3.513094e-13, 1.128057e+19, 4.199038e+13, 7.553080e-20, 4.380028e-11, -2.502103e-19, 5.943049e+15, -1.266134e-10, 4.825578e-09, -2.778134e-16, 1.881866e-10, -3.677556e+08, -2.166345e-10, 3.919158e+05, 2.778912e-07, 1.822489e-05, 1.513496e-01, 9.327925e+05, -4.050132e-14, 3.311913e+01, 9.290544e+15, 1.302267e+03, -1.252080e+17, -4.208811e-04, -3.225464e+16, 2.093787e+16, -3.352116e+07, 4.797665e+15, -1.539672e-17, 4.835159e+04, 2.446236e-07, 2.355328e-17, 2.044244e-12, 3.210415e-11, -1.322741e+16, 5.538184e-14, -4.612046e-05, 4.758939e+15, -2.038208e-10, -2.451148e+18, -2.699711e-19, -2.019804e-09, 5.631634e-13, -2.288031e+05, -3.211488e+12, 7.511869e+13, -3.209453e-09, 3.806128e-18, 4.025006e-14, -1.700945e-10, 4.136280e-13, 4.517870e-04, 2.739233e+11, -3.736057e-03, 2.255379e-20, 3.122584e-16, 3.192660e-18, 4.765755e-09, 2.396494e-13, 1.625326e+02, -3.413821e-18, 3.627586e+10, 8.708108e+07, 2.244241e-09, 3.718827e-02, 1.803394e-18, 4.377806e-04, 1.593155e-04, -2.886859e+19, 2.446955e-06, 4.714172e-07, -1.444181e+14, 5.921228e-22, -3.968436e+05, 2.081487e+08, 4.200042e+18, -1.334353e-20, 1.637913e+12, -7.203262e+03, 3.510359e+09, 5.945107e-08, 2.798793e-07, 1.819020e+17, -1.331690e+02, -2.714485e+18, -2.344350e-18, -1.313232e-20, -6.739364e-22, 1.025007e-02, 1.186976e+07, -1.412268e+09, -6.194861e-18, -4.523625e-03, -4.504270e-06, 2.158726e-21, -8.330465e-17, 4.566938e+11, 6.677905e-05, -2.312717e-13, 5.325983e+16, -1.075392e-04, 1.140532e-13, 2.606136e-11, -2.815243e+16, -3.550714e-16, -1.033372e+05, -1.183041e+03, -7.872171e-21, -4.362058e-07, -3.181126e-07, -2.676671e+18, -2.674920e-15, -3.991169e-16, -4.401799e+07, -2.826847e-10, -2.033266e-20, -5.669789e-11, 3.711339e+05, -1.194584e-17, -3.310173e+10, -1.743331e-15, -2.288755e+15, 8.610375e+06, 4.796813e+07, -1.465344e+07, -4.074823e-12, 2.089962e-21, -4.171761e-18, -4.682371e+18, 4.030447e+08, 4.679856e-07, -2.662732e+15, 2.551805e-21, 2.482089e+05, -2.310281e-10, 3.533837e-08, 1.829437e-07, 3.074466e-06, -2.889997e-12, -4.203806e+01, 1.598374e-21, -1.300526e-05, 2.921093e+14, -8.847920e+14, 3.788583e-04, -4.538453e+19, -2.734893e+07, 1.351281e-04, 1.128593e-01, 3.868545e+13, -1.200438e+18, -2.641822e+10, -4.493835e-16, -6.291094e-13, 2.534337e-08, -4.063653e-03, 3.200675e-02, 2.243642e+08, 5.170843e-08, 8.984841e-14, 2.228243e-01, -6.770559e-09, 3.513375e-16, -2.512038e-14, 3.421696e+04, -4.514522e+01, -1.062799e-20, 2.853168e-19, 8.503515e-21, -1.664790e-03, -2.515606e-18, 1.237958e-21, -8.059224e-20, 4.386086e+00, 5.301466e+17, 4.388106e-12, -3.432129e+00, 2.189230e+18, -1.806446e-02, 3.266789e-18, 3.355664e-13, -1.206966e-21, -4.813560e-02, -1.352049e+18, 1.257234e-07, 2.511470e-09, -2.512775e-01, 3.613773e-10, -9.065202e+16, -1.777852e+18, 1.444606e-01, -2.857379e+00, -1.912993e+00, 3.436817e-09, -1.749039e+14, 2.215154e-18, 3.384923e+18, -4.513038e-09, 4.814904e+05, 3.730911e+15, 1.861706e+12, 3.378290e-03, 2.851468e-06, -1.577518e-04, -4.122504e-12, -2.743002e+03, 8.512568e-02, -1.333039e-09, -4.899609e-17, -1.782085e-11, 2.552482e-02, 4.200193e+10, -4.298147e+03, -1.923210e-10, -1.208889e+01, 4.606772e-21, -3.331241e+10, -3.704566e-16, -3.733178e-20, -4.950049e+16, 3.184384e+15, -4.107375e-06, 1.801875e+09, 9.632951e-16, 7.172728e-10, 2.324621e+07, 2.892586e+15, -1.582511e-17, -4.119044e-13, -1.248361e+09, 1.531907e+08, -1.795628e-19, -1.735919e-17, -4.646689e-07, -2.779304e-11, 8.048984e-10, 3.536087e-02, -6.494880e+18, 2.714073e+06, 3.374557e+18, 3.621468e-06, 2.742652e-07, 2.551176e+03, -4.420578e+18, -4.370624e-08, -4.507765e-11, 4.193746e-20, 1.206645e+13, -3.750231e+03, 4.390893e+08, -9.756466e+11, 3.392778e-06, -3.453465e+01, -1.406102e+11, -3.673526e-15, 1.417082e-03, 1.499926e+16, -4.471032e-17, -2.657920e+16, 4.792261e+09, -3.212735e+17, -3.372737e-05, -4.730048e+01, 3.365478e+07, 2.835695e+13, -3.242022e-07, 3.640288e+11, 1.862055e-08, -4.121250e-19, -3.891100e-02, -4.367058e-15, 1.364067e-17, -4.575429e-12, 3.621347e-07, 1.506864e+11, 3.715065e+18, -1.773352e+08, -3.502359e+07, -2.326890e-04, 2.948814e-17, -2.438988e+14, -2.994787e+04, -3.755515e+12, 2.708013e-13, 3.281046e-01, -3.710727e+12, -8.380304e+14, 1.062737e-05, 2.385939e+16, -4.383210e-20, -3.779417e+03, 3.080324e-03, 3.810188e+16, 3.058415e+00, -2.484879e-21, -1.951684e+01, 6.979033e-10, -3.866994e+06, 4.278936e-19, 9.365131e+10, -3.685205e+01, -2.678752e-16, 2.011434e-19, 1.884072e+08, -1.300910e+04, 2.414058e-09, -4.675979e+11, 3.583361e-19, -4.499438e+18, 1.641999e-21, -2.686795e-10, 6.136688e-20, -3.793690e+16, 4.944562e-20, -3.490443e-03, 3.080547e+02, 2.041413e-06, 2.021979e+03, 2.314233e-06, 1.564131e-01, -8.712542e+17, 7.569081e+16, -1.056907e+17, 2.095024e-14, -2.487621e+17, -3.490381e+19, -6.944641e-01, -2.892354e-08, -3.597351e+12, -1.985424e+06, -2.348859e+09, -1.657051e+01, -3.358823e+14, 3.219974e-16, -4.819092e-13, -2.905178e-11, 8.257664e+04, -4.092466e-15, -3.464711e-13, -3.956400e-14, -2.548275e-08, -8.917872e-21, 7.387291e+13, 2.300996e+16, -4.870764e+18, -9.909380e-03, 1.260429e-08, -3.409396e-12, 1.003848e+02, -4.883178e-02, -3.125474e-14, 1.005294e+11, -4.736012e+09, -1.647544e-09, -3.491431e-03, 4.619061e+07, -4.547601e-09, -3.788900e-02, -2.648380e-17, 4.601877e-16, 1.754357e+13, 4.325616e+12, 1.860822e+03, 4.080727e+15, -4.573470e-14, -1.293538e+16, 2.811449e+05, 4.032351e+06, 4.274005e+04, 3.454035e-21, 4.933014e+09, -3.712562e+08, 3.158678e+06, -1.636782e+11, -2.884298e-18, -3.685740e-17, 1.027472e-07, -3.765173e-12, 2.740894e-17, 2.634880e+02, -4.334010e+00, -3.708285e-14, -3.858731e+16, -3.956687e+13, -4.064064e-12, 2.558646e-05, 4.459143e+03, -9.661948e+03, -1.994335e+16, 1.202714e-17, -3.782707e-17, 9.099692e-04, -1.864561e+09, 3.493877e-08, 4.288188e-01, 1.767126e-14, -6.779451e-22, -1.977471e-09, -3.536454e+06, -7.319495e-04, 2.004028e-16, -3.181521e-17, 3.336202e+14, -2.752423e+07, 3.390953e+01, 4.199625e-15, 2.883232e-12, 3.122912e-06, 7.324619e-19, 3.092709e-02, -2.758364e-15, -2.489492e+12, -1.622009e-08, 2.371204e+06, -1.582081e+08, -6.382371e-17])

    @property
    def d3(self):
        return [2.047398e-20, 2.091541e-20, 9.084241e+14, 1.583413e+01, 5.168067e-02, 1.360920e-11, 9.818531e-21, 6.293083e+07, 4.406956e-14, 8.540213e-09, 7.329310e-03, 5.566796e+00, 3.968358e-08, 4.928656e-08, 5.994301e-20, 8.281551e-21]
    @d3.setter
    def d3(self,value):
        ca(value,[9.025110e-18, 3.567231e+17, 2.594489e+01, 2.311708e-04, 7.345164e+13, 6.550284e-01, 1.969554e+12, 9.451979e-05, 5.900637e-09, 9.975667e+03, 6.549533e-17, 2.227145e-13, 2.822132e+18, 4.332600e+18, 1.485466e+05, 5.844952e-14])

    @property
    def d4(self):
        return [2.864760e-08, 3.900663e+13, 9.105789e+11, 2.943743e-15, -2.823159e-16, -3.481261e+19]
    @d4.setter
    def d4(self,value):
        ca(value,[-4.207179e-09, -3.611333e+11, -4.155626e-06, -2.458459e+10, 2.826045e-11, 3.511191e-08, 4.759250e-07, 2.455883e+09, 4.182578e+11, 4.732337e-14, -2.967313e+02, -4.139188e+14, 6.287269e+03])

    @property
    def d5(self):
        dat=numpy.array([4.427272e-10, -1.149547e-08, -1.134096e+16, -4.932974e-03, -7.702447e-01, -3.468374e-03, -5.037849e-14, -4.140513e-08, 4.553774e+03, 2.746211e+01, -4.388241e-17, 2.262009e+00, 5.239907e+06, 4.665437e-05, -1.662221e-05, 5.471877e-13, 2.592797e+11, -4.109763e-05, 1.797563e-04, 1.654153e+01, 4.011197e+07, -2.261820e-10, 5.836798e+02, 1.518876e-18, 4.814150e+18, -4.610985e-07, -3.126663e-07, -1.981883e+10, 4.117556e-02, 1.937380e-07, 1.397017e-10, 2.809413e-17, 9.387278e+18, 4.777753e-11, -4.248411e+15, 3.851890e-16, -1.598907e-08, 3.699930e+14, 2.763725e-08, -4.130363e+17, 3.105159e+06, -2.026574e+00, 3.956735e+01, 3.893311e-04, 3.574216e+13, 3.618918e+03, -4.027656e-09, 9.174470e-02, -8.108362e-21, 1.857260e-18, -3.540422e+13, -2.985196e+12, -3.219711e-08, -1.618670e-13, -2.648920e+12, 1.224910e-14, -4.740355e-03, 4.604337e-18, 3.809723e+05, -4.460252e+15, 1.894675e-15, -4.141572e-08, -3.939165e-09, -1.916940e-06, -2.382435e+16, -4.689458e-01, 1.498825e+17, 1.876067e-15, -1.801776e+09, -1.140569e-05, -6.881731e-08, -4.835017e-07, 3.843821e-17, 2.220728e+06, -4.321528e+10, -3.950910e+01, -1.732064e-11, 3.009556e-16, -3.509908e+18, -7.781366e-15, -2.511896e-18, -2.037492e+04, 2.656214e-19, 2.163108e+16, 4.526743e+19, 2.738915e-11, 8.491186e-16, -1.286244e+05, 3.635668e+12, -4.964943e+15, 3.725194e+05, -4.010695e-19, 2.140069e-09, 3.957374e+19, 4.478530e-06, 4.284617e-06, -3.459065e+12, 1.525227e-18, 4.892990e+06, 3.557063e+07, 2.986931e+18, 2.147683e-05, -4.190776e+17, -3.715918e-14, -3.448233e+01, 1.272542e+15, -3.900619e-06, -3.712080e+05, 3.388577e+04, -4.440968e-11, -4.395263e+18, -4.052174e-06, -3.065725e+00, 3.915471e-04, 4.863505e+12, 4.861871e-09, 4.607456e+03, -1.845908e-12, -9.985457e-11, -4.534696e-08, -1.163049e-17, 4.492446e-11, 3.078345e+06, 8.520733e+05, 2.218171e+14, -4.546400e+09, 4.641295e+09, -1.677260e-07, 9.650426e+04, -4.001218e-04, 4.761655e-22, -3.989865e+01, -5.800472e-08, -2.548565e-01, 4.648520e-08, 4.255433e-16, -2.387043e-11, 4.172928e+17, 4.194274e-12, -1.391555e-04, -1.063723e-01, 1.609824e-13, 9.196780e-10, -4.744075e+06, -4.764303e-02, -4.540535e-10, -4.361282e+00, -1.460081e+01, -2.215205e-16, 4.652514e-19]) + 1j*numpy.array([-3.227745e-11, 3.306640e+04, 5.733779e-03, -4.965007e+12, -1.568029e-15, -3.008122e+08, -2.135053e-06, -2.406927e+10, 3.292783e+05, 4.388607e+01, -1.765870e+18, -1.356810e+11, -1.227140e-17, -4.613695e-13, -2.700191e-03, -3.556736e-15, -2.019073e-03, -4.766186e+11, 6.689841e-18, 3.052622e+03, 1.277135e-05, -3.121487e+15, -3.821687e+10, 1.168559e+17, 3.894338e+02, 1.815897e-01, -2.028013e-16, -1.291271e-04, -4.564800e+01, -1.537011e-11, 2.585832e-08, -1.369181e-21, -1.508252e+19, 7.819509e+14, -8.344493e+11, -3.658894e-04, 3.591114e+08, -3.293697e+00, 3.409179e+08, -3.879994e+18, 3.766739e-07, 2.334020e+17, -3.558653e-14, 4.718551e-03, -4.986314e+05, 7.019211e-03, -4.789392e-02, 1.732946e-11, 2.863924e+06, 4.353270e-09, -2.371537e+06, 3.279747e+07, -4.805626e-20, 2.621159e-16, 3.031856e-04, 1.224164e-13, -5.887172e+11, -2.589087e-05, -2.936782e+18, -1.259862e+08, -2.475554e-02, -3.565598e+04, 1.708734e+00, -1.844813e+00, 3.616480e+10, 3.944236e-01, 3.669220e+06, -3.385628e-15, -2.178730e+01, 4.619591e-17, 2.250613e-10, 7.894372e+11, -3.258819e-19, -3.287104e+01, 4.524240e-14, 3.506383e-08, -1.023590e+02, -1.400509e-20, 3.294976e-07, -3.740683e+07, -1.408191e+04, -4.009454e-12, 3.780340e-11, -1.697898e-04, 3.329524e-02, -2.017186e-08, -4.107569e-09, 3.223035e-18, -2.305074e+12, -4.410777e+09, -1.776812e+05, -2.204486e+03, 3.928842e+00, 8.164433e-19, -3.205076e-12, 4.395648e-17, -4.112187e-04, 3.032568e+19, -1.555449e-04, -1.139386e+19, 1.296998e+15, 2.120574e+06, -3.686849e+05, -2.367773e+08, -1.322619e+10, -4.118283e-11, 4.910520e+08, 2.833307e+14, 1.921342e+02, 3.152412e+19, 1.676044e+05, -3.724410e-18, 2.819222e+04, 2.091958e+00, -4.193395e+05, -4.363602e-11, 4.613626e+02, 1.208108e+18, 1.149369e-01, 1.258756e-07, 3.502706e-04, 1.020676e-19, 2.822635e-03, -1.578762e-14, -4.171860e-19, -2.410204e-16, -2.000543e+13, 3.060033e+16, 4.215806e+09, -3.419002e+13, -2.856480e-11, -2.210954e-12, 3.305456e+03, -3.624269e-13, 3.099517e-05, -1.411512e-10, -1.566814e-06, -9.637734e-19, 8.972782e+09, 4.064705e+08, 4.784309e+14, -8.230735e-01, 2.129415e+19, -3.169789e+05, 8.918012e-19, 2.172419e-18, 4.803547e-17, 1.503276e-10, 4.251650e-21, -4.256823e-12])
        return dat.reshape([5, 6, 5],order="F")
    @d5.setter
    def d5(self,value):
        ca(value.shape,[8, 6, 2])
        ca(value.real.flatten(order="F"),[-5.528040e-08, 3.832644e-01, -9.139211e-22, -4.919312e-05, 3.809620e-11, 1.751983e-09, 2.207872e-21, 1.432794e+09, -1.970313e+11, 3.405643e-18, -3.756282e+14, -4.918649e+08, -3.162526e-14, -2.853298e-09, 2.835704e+10, 4.458564e+16, 6.657007e+09, 3.640798e-10, 4.950898e-06, 3.384446e+14, -4.065667e+16, -2.243648e-05, 4.822028e-21, 4.231462e-14, -2.526315e+11, -5.626782e-05, 2.321837e+13, 1.772942e-09, 1.606989e-08, 2.669910e-04, -3.635773e+08, -3.967874e-10, 6.599470e+15, 4.612631e-08, -1.417977e-11, -8.066614e-18, 5.738945e+15, 6.408315e+13, 1.922621e+12, 3.096211e-14, -2.079924e+18, 1.664290e+09, -4.502488e+07, 3.092768e+05, 4.414553e+10, -3.673268e+02, -4.772391e+17, -1.100877e+02, -1.453900e+01, 4.293918e-13, -4.270900e-02, -3.886217e+11, -2.206806e+02, 7.034173e-07, -2.826108e-21, 3.616703e-21, -3.385765e+04, -7.027764e-11, 9.684099e+05, -4.248931e+03, -3.415720e-20, -3.315237e-11, -9.555895e+11, 3.520893e-13, 1.089514e-13, 3.591828e-21, -4.847746e-06, -2.678605e-16, -7.480139e-04, 2.208833e+01, 1.075027e-07, -1.047160e-05, 2.309356e+06, 7.308158e-19, -4.915658e+02, 4.634137e+18, -3.682525e+13, 4.124301e-06, 4.158100e-10, 2.091672e-11, -6.856023e+07, 8.418116e-07, -1.655783e-13, -2.502703e-03, 1.274299e+17, -4.784498e-20, 1.357464e-10, 4.107075e-13, -2.753087e-05, -2.594853e-14, -3.712038e-13, 1.143743e+14, -2.495491e+10, 2.331111e-15, 2.987117e+18, 2.876066e-18])
        ca(value.imag.flatten(order="F"), [-8.370342e-05, -2.348729e+14, 3.257323e-03, 4.131177e+03, 2.161235e-13, -4.721350e-09, 1.995494e+02, -3.671161e+01, 3.577448e-08, -2.106472e+17, 4.470172e-10, 4.042179e-18, -6.516616e+06, -3.452557e+08, -2.995060e-12, 7.108923e+00, -3.211521e+12, -3.543511e+12, -4.990060e+10, -1.078185e+12, -4.563018e+11, -4.127342e-07, 3.047283e-13, -7.096004e-20, -3.751135e+15, -1.121229e+06, 2.090954e-11, -2.086763e-11, 4.890986e+07, -2.309172e+13, 1.621930e-07, -4.366606e+11, 3.614235e+10, -1.482655e+07, -2.064002e+14, 4.607724e-09, 1.349841e+16, 2.340153e-02, -4.978818e-20, -4.310755e-08, -3.092006e+17, 2.129876e-14, 3.521718e-09, 1.785216e-09, 3.359563e+13, 4.071776e-16, 1.436872e-20, -3.517250e+05, 5.252845e-07, 7.469291e-01, -4.355370e+18, -1.421206e+15, 1.153528e+15, 7.734075e+01, -4.073023e-10, -4.657975e-13, -4.290567e-03, -4.795922e-13, -5.476246e+01, -4.044947e+00, 2.545910e-04, 3.937911e+13, -9.652266e-02, -5.878603e-07, 1.205180e-04, 4.153653e+16, 4.943621e-18, 4.347876e+13, 4.479099e+04, -3.199240e-04, 2.432062e+06, 2.478472e-20, 4.684549e-17, 3.321873e-04, -3.465954e+04, 4.173493e+02, -2.258389e+19, 3.365401e+10, -2.122599e+09, -2.071802e+06, 2.590336e+09, 3.335575e+06, -4.325264e-03, 4.529918e+14, -4.182319e-18, -3.928899e+02, -2.170676e+06, -1.918490e-17, 1.227619e-21, 2.607308e+04, -2.312853e-15, 4.028300e-17, -3.146932e-11, 9.543032e-05, -4.535571e+12, -3.423998e-17])

    @property
    def s1(self):
        return 7.8573
    @s1.setter
    def s1(self,value):
        pass

    @property
    def s2(self):
        return [3.252887e+09, 1.028386e-04, -2.059613e+01, 1.007636e-14, -4.700457e-13, -1.090360e-22, -3.631036e-15, 2.755136e-09, 4.973340e+13, 2.387752e-15, -9.100005e+06, 1.484377e+13, -2.287445e-13, -3.718729e+18, -4.771899e+19, 8.743697e+13, 1.581741e+07, 2.095840e-09, -5.591798e-03, 6.596514e-06, -1.006281e+05, -4.126461e+12, 4.246598e-20, -1.376394e+08, -3.398176e-03, -1.360713e-21, 3.109012e+14, -8.112052e+07, -8.118389e-02, -3.455658e+14, 7.352656e+12, 4.198051e+06, 4.258925e-03, -2.634416e+12, 3.362617e+02, -4.606198e-15, 4.228381e-19, 4.209756e-15, -1.268658e+05, 3.019326e+02, 7.937019e-01, 6.225705e-09, 1.324805e-19, -4.355122e+01, -4.533376e+15, -1.584597e+01, 1.657669e-02, -3.720590e-18, 2.038227e-04, 2.890815e+04, 1.513743e-14, 4.993242e-20, -5.255463e-21, -8.084456e-14, 4.087952e-09, 2.518775e-21, 4.977447e+15, 3.363414e-19, -3.931790e-20, -7.810002e+14, -3.589876e+14, -4.969319e-18, -4.356951e-20, -3.682676e+02, -1.319524e+10, 3.805770e-11, 2.134369e-10, 3.684259e-08, -2.901651e-13, -4.486479e-01, 2.208715e-02, 3.224455e-01, -3.305078e+09, -3.326595e-02, -2.473907e+03, 3.608010e-15, -2.596035e-01, 2.594405e-01, -7.569236e-01, -3.430125e+09, 2.920327e+02, -3.763994e-12, 2.617484e-12, 4.808183e-07, 3.885462e+15, -1.201067e+00, 1.887956e+06, -4.038215e+02, -4.710561e+03, 1.659911e-16, -4.955908e-17, 4.681019e-09, 3.945566e+05, -3.433671e+19, -2.679188e+05, -2.357385e-01, 2.891702e-19, -4.464828e-06, -6.003872e-04, 1.369236e+18, -3.597765e+01, -4.246195e+08, -4.765202e+17, 4.472442e+10, -1.038235e-05, -4.632604e-09, -2.484805e-15, -7.998089e-16, -3.690202e-04, -3.276282e-04, 1.966751e+10, -5.081691e-18, -2.004207e-05, -2.756564e-03, -2.624997e+14, 2.398072e-20, -4.098639e-10, 2.930848e+01, 8.983185e+15, 1.984647e-15, 1.331362e-16, -6.519556e+15, 4.270991e+15, -9.165583e-13, 4.266535e+17, 4.238873e-21, -2.487233e+17, 4.904756e+03, 2.692900e+10, 1.467677e-18, -2.204474e+06, -1.806552e-09, 9.617557e+17, -1.988740e-20, 1.713683e-04, -2.360154e-21, 4.178035e-17, 2.600320e+12, -4.761743e+09, 3.034447e-20, 4.941916e-06, -1.373800e+04, 1.851938e-09, 1.304650e+14, 3.067267e+07, -4.100706e-06, 2.190569e-03, 5.901064e-17, -2.152004e+15, 4.050525e+04, 3.769441e-06, -4.388331e-12, 1.037797e+12, 3.512642e-19, 3.857774e-09, 1.036342e+03, 3.683616e-18, 9.785759e+10, 2.199992e+03, -2.435347e-02, 1.526312e+06, 2.569847e+14, -2.288773e-01, 4.724374e-06, -3.807381e+13, 2.924748e-10, 2.820652e-20, 4.835786e-12, 2.811112e+02, -6.431253e+02, -4.843622e-06, 1.676490e-10, -4.432839e+07, 1.661883e+19, 8.668906e+07, 2.256498e-04, 2.170563e-01, 1.013347e-17, -4.271306e+11, -2.431836e-17, 3.983056e+02, 4.236306e+05, -2.142877e-20, -2.760277e-12, -8.479624e-08, 2.903436e+05, -3.288277e-17, 4.173384e-10, -1.598824e-08, 8.702005e+05, -1.456065e+08, 2.035918e+06, -1.445426e+02, -4.148981e+05, 4.439242e+02, -1.223582e+16, -8.226224e+14, 1.690797e+16, 1.683472e-04, -4.809448e-16, 4.517499e+06, 4.369645e+02, -4.532906e+09, -3.539758e+07, -2.406254e+01, 4.396602e+00, 2.995832e-01, -2.953563e-04, 3.412885e+17, 1.386922e-17, -2.177566e-04, 2.548426e+04, -3.937000e+16, 2.578962e+02, 2.423257e+16, 3.069379e+09, -4.940417e+09, -4.618109e-13, -1.387521e-11, -2.168721e-05, 1.917758e-01, -3.144071e+03, -1.045706e-13, -2.869528e+02, 2.072101e-13, 4.267714e+12, -2.063457e-19, -3.025547e-12, 8.101894e+10, -4.196343e-04, 4.753178e+18, -2.286673e+08, -2.618986e-10, 3.949400e-10, -4.390776e+12, -2.498438e+10, 3.800599e+12, -3.704880e+15, -4.173265e+02, 3.326208e+19, -1.093729e-21, 3.042615e+16, -1.711401e-09, 3.039417e-19, -2.250917e+15, 2.195224e-01, -2.953402e+05, -1.486595e+17, -2.387631e+00, -1.634038e-14, 6.153862e-18, -3.842447e+05, 3.238062e-14, -4.341436e-11, -1.816909e-19, -3.534227e+14, 8.578481e+07, -4.067319e+09, -4.680605e-08, 4.050820e+04, 1.715798e-11, -5.232958e-12, 2.291111e-07, 1.086749e+01, -3.028170e-14, -6.277956e+13, -1.639431e+11, 4.158870e+17, -1.208390e-18, 4.835438e-05, -3.135780e-08, -4.087485e-12, 2.466489e-08, 1.949774e+00, -3.532671e-21, -1.422500e+12, 4.352509e+03, -1.444274e-17, -1.162523e+19, -4.815817e-07, -2.809045e+11, -1.212605e+03, -3.496461e-08, 6.743426e-18, -4.226437e-06, -3.627025e+07, 1.037303e-05, 2.411375e+08, -2.721538e+12, -4.809954e-06, 4.578909e+16, 9.257324e+06, 4.326725e-03, 4.416348e+12, 4.424289e+13, 3.180453e+12, -6.028285e-10, 3.344767e-14, -2.747083e+18, 1.133844e-15, 3.922737e-06, -3.199165e+00, 2.417553e+02, 3.015159e-20, 2.119116e-02, 4.019055e-09, 3.368508e-21, -1.613240e-19, 3.832120e-14, 1.202460e+17, -3.304317e+19, 1.692435e+17, -2.597919e-05, 3.916656e+17, 4.821767e+06, 4.372030e+02, 1.987821e-08, -1.976171e-08, 1.319708e-09, -4.213393e+10, 3.829773e-15, -4.762296e-21, 4.642216e-18, 1.662453e-13, 6.642151e+03, 2.539859e-02, -3.112435e+09, -3.627296e-20, -1.660860e+02, -3.678133e+07, 3.428538e-01, -2.277414e-20, 2.228723e+17, -2.833075e-06, 9.084647e+03, -2.976724e-16, 2.778621e+15, -2.806941e+07, -1.626680e-15, -4.658307e+13, 7.967425e-11, -2.793553e-21, 4.778914e+16, -6.145348e-21, -4.883096e+11, 1.338180e+04, 7.533078e-16, 3.252210e+05, -2.882071e+10, -2.754393e-06, -1.689511e-16, -1.979567e-10, 4.494219e-04, 3.285918e-15, -4.347530e+05, -1.085549e+15, 1.301914e+07, 3.855885e+13, 3.036668e-11, -4.706690e+12, 3.727706e+17, -4.446726e-12, -4.829207e-08, -1.543068e-10, -2.473439e-11, -2.718383e+13, -4.211115e-21, 3.327305e-04, -1.084328e-20, 3.849147e+06, -1.321415e+09, -3.518365e+07, 2.246762e-21, 2.482377e+11, -4.265765e+03, -4.538240e-05, 2.727905e+18, -2.383417e-13, 4.103955e+04, 8.015918e-06, -2.965433e-18, 3.156148e+03, 8.093784e+18, 4.868456e-12, 1.048517e-02, 1.112546e-19, -3.751041e-12, -3.734735e-06, 3.019242e+06, -1.480620e-17, -3.405209e+07, -1.123121e+19, 8.155940e-20, 1.406270e-17, 2.154811e-13, 9.943784e-20, 1.523222e-17, 6.987695e-21, 8.826612e-12, -2.325400e-20, 3.700035e+15, -5.559864e-11, -8.568613e+10, 1.434826e-07, -2.080666e-03, -2.548367e-03, -4.310036e-18, 3.104310e+00, -3.862149e+17, -4.092146e-13, 3.538555e-14, -4.950494e-05, 6.538592e-13, -4.196452e-11, 2.351540e-01, -1.232819e-01, -3.669909e-21, 1.528733e-14, 5.661038e-15, -1.967561e-07, -2.284653e+02, -1.834055e-10, -2.175838e+05, 4.247123e+06, 1.184396e+18, 4.156451e+15, -4.992962e-14, -2.351371e+06, -6.698828e-10, 2.897660e+17, -3.470945e-06, 4.630531e-07, -4.453066e+10, 4.069905e+09, -4.459990e-08, 4.702875e-13, -2.780085e+17, 1.293190e-05, 2.227539e-03, 1.534749e-21, 7.390197e-02, 4.522731e-10, -1.224482e-02, -3.996613e+02, -1.057415e-15, -7.371987e+14, 4.291850e-02, -4.243906e-08, -3.540067e-04, 4.535024e+09, -3.027997e+10, -3.986030e-02, 1.722268e-04, -3.140633e-20, 3.343419e+08, 4.713552e+14, -3.190084e+05, 2.449921e-01, 2.727707e+14, -3.545034e+11, 2.417031e+13, -2.231984e-09, 3.533907e+16, -4.662490e+16, 3.355255e+14, -1.567147e+17, -3.525342e+12, -3.586213e-16, -4.002334e+15, -1.928710e+08, -4.718466e+04, -1.539948e-06, 3.135775e-11, 3.862573e-10, -3.105881e+08, 4.421002e-05, -2.369372e+01, 4.758588e+13, -1.044237e-15, -4.535182e-10, 1.330691e+18, 3.636776e-01, -4.068160e-12, 2.757635e-17, 3.247733e+13, 1.247297e+06, 5.806444e-13, 3.521773e-05, 4.589556e-14, 1.582423e+00, -1.676589e+00, -3.864168e-07, -3.042233e-02, 2.007608e+14, 4.852709e+02, -2.817610e-04, -1.882581e+19, 1.057355e-14, 4.090583e-04, -1.848867e-13, -5.463239e+13, -1.041751e+05, 3.457778e-01, -2.562492e+00, -6.751192e-10, 1.688925e-21, 3.884825e-07, 1.592184e-12, -2.039492e+06, -1.196369e+19, 2.200758e+00, 2.550363e-21, 7.597233e+06, -1.929970e+09, 1.939371e+03, -3.236665e+09, -1.313563e-13, 2.007932e+02, -3.028637e-02, -1.532002e+00, 2.165843e+17, -3.511274e-04, -3.777840e+15, 1.645100e+17, 3.088818e-07, -2.793421e-11, -4.286222e-01, 4.385008e-10, -2.105222e-01, -2.212440e+08, 2.684288e-01, 1.407909e+18, -3.881776e+08, 3.505820e-09, 3.555082e-19, 3.573406e+01, 4.042915e-19, 2.066432e+08, -2.467607e+10, 3.453929e+01, 4.297309e-14, 1.256314e-11, 8.930289e+14, -3.662200e-03, 2.075690e-16, -2.866809e-17, 4.394016e+10, -2.014195e-03, -3.738633e+12, -4.953528e-05, 3.710240e+06, 3.319208e+04, -5.762511e-20, -4.690619e+16, 3.412186e+19, -1.241859e+09, -4.081991e+12, 4.622142e+03, -1.285855e-02, 1.532736e-08, -2.364101e+09, -1.369113e-18, -2.168979e+19, 2.952627e-14, -2.358172e-16, -1.992288e+00, -9.180203e+12, 1.675986e+07, 4.817708e+06, -1.624530e+06, 4.857415e-01, -5.995664e-03, 1.874911e+08, -3.320425e-17, 5.469104e-02, -3.069767e+11, 8.084999e+12, -2.321768e-20, 1.920249e-06, -4.114087e-02, 3.244903e-04, 3.203402e-17, 4.143519e+06, 4.093124e+17, 4.456464e-15, -2.262509e-13, 4.856535e-08, -4.550552e-15, -3.011803e+18, -2.882488e+13, -2.690616e-04, -3.996010e-19, -4.438855e+18, -1.942208e+03, 1.934537e+18, -1.961547e-07, 4.970021e+17, -3.531211e-17, 4.187133e+04, 2.854106e-12, -2.313257e+13, -3.471439e+16, -6.829753e-16, -4.338617e+03, 5.552258e+05, 1.520718e+19, -2.527013e+14, -2.732660e-09, -1.957740e+11, -4.767907e+12, -4.837256e+18, 3.155432e-12, -3.278156e-04, -1.117720e-13, -3.838176e+11, -7.207202e+08, -4.075808e-21, 1.659402e-14, -4.301886e-19, -4.461337e-11, 2.200979e+15, 4.339143e+07, 5.071459e-06, 1.832776e+18, -2.698948e+03, 4.682397e+01, 2.801081e-08, -3.424292e+00, -5.130555e+14, 1.229975e-14, 2.383361e-09, -3.611087e-07, -2.576595e-07, 1.295398e-08, -2.525216e-11, -2.546657e+10, 9.501518e+03, 8.325605e+04, -1.382092e+02, 2.169085e-21, 4.019485e+16, -2.404251e+17, 1.154833e+10, 9.454498e+01, -7.888753e-09, -4.907318e-20, 1.373262e+08, -2.295105e-21, 1.329034e+17, -3.403883e-20, 3.500734e-03, 2.657397e-20, 4.956090e-07, -2.191353e-03, -1.879262e+09, 4.519858e-14, 4.592234e-14, -1.473612e+11, 4.425251e+10, -3.936903e-01, -2.866089e+09, -3.046203e-09, -4.818832e+01, 2.460150e+02, 2.944622e-11, -1.675111e-20, -1.206111e+01, 5.044200e-13, 3.225861e+02, 3.170008e+12, 1.964043e-20, 3.464033e+03, 1.286135e-08, -6.425529e-10, -4.630162e-02, 2.616476e+18, 4.853669e+03, -1.851316e-03, 1.262159e-02, -1.816675e-12, 3.753560e+14, -3.033601e-18, 1.915137e-02, 3.411614e-14, 4.849348e+05, 3.033922e+13, 3.174852e-17, -4.397997e-09, -9.549484e-01, -1.706859e+11, -3.009122e-01, -8.189854e-15, 4.122789e-17, -1.351025e-13, -2.365671e-10, -1.139709e-05, -2.020593e+10, 3.664729e+14, 1.170917e+00, 1.157248e-19, -4.189734e+17, -4.407278e+13, 4.776929e+18, -3.279961e+07, -4.740186e-15, -3.764392e-02, -2.193781e+18, -4.556987e+00, -3.170243e-18, -1.755775e-16, -2.163959e-03, 2.410150e+11, 1.215874e-18, -4.927956e-05, 2.252375e-06, -3.315242e-14, -3.476357e+16, -4.545391e+00, 6.072704e-13, -4.571860e+09, -2.297081e-02, 2.401997e+10, -6.449709e+05, -3.580234e-08, -5.390535e+08, -4.891390e-19, 3.441769e-09, 4.885513e-09, -4.897531e-10, -1.792753e+08, 2.048965e+13, 3.339876e-21, 4.140957e+04, 2.022520e-21, 5.983159e+06, 1.938164e+13, 2.796107e-19, -1.975692e+09, -2.106710e+15, -4.482226e+09, -2.968068e-19, -1.171747e-03, 1.579378e-01, -4.568752e+16, 2.593340e+11, 3.441530e+10, 3.461992e-01, -5.333082e-09, -4.611969e-12, -4.262468e+19, -4.367063e+01, -2.447378e-11, -3.554859e+02, 4.824680e-05, -1.122071e+11, -2.226371e+13, 3.917182e-17, -1.308204e+10, 4.105055e-16, 5.087060e+07, 7.102691e-05, -2.872202e+03, 1.711266e+11, 3.331993e-08, -1.313944e-08, 3.648109e+11, 5.394321e+01, -4.125398e+03, 3.460645e-02, 2.573745e-18, -1.376298e+01, -3.283028e-05, 3.939711e-12, 3.986184e+17, 2.619889e-11, -4.318052e-09, 1.410821e+00, 3.547585e-07, 4.046432e-17, 1.880087e-07, 1.867841e-05, -1.383592e-21, 2.972106e-05, 2.867092e+01, 3.092781e+03, -6.897683e-02, -1.707761e-04, -4.231430e-11, -3.796784e+00, -2.953699e+11, 3.691013e+09, -3.962307e-12, -1.335633e-17, -1.759192e-01, -4.332862e+04, 1.044899e+11, -2.126883e+03, 1.948593e+14, -2.173759e-05, -4.393250e+05, 1.626217e+08, 2.832086e+18, 4.655433e+03, 2.944186e+08, 2.864233e+03, -3.565216e+05, -4.667000e+11, -3.739551e-03, 3.137195e+05, 2.044129e+19, 2.629232e+14, 3.119859e-09, 3.656121e-15, -4.844114e-03, -2.641449e-11, -3.788231e+05, 2.803203e+17, -3.764787e+09, -6.009761e-08, 4.106308e+01, -2.071363e-20, 1.884576e-20, 2.654081e+11, -3.456281e-11, -4.760486e-02, 4.096057e+11, 4.346738e-11, 2.827941e-02, -1.946717e+08, -9.067051e+15, 4.331454e-14, 4.792779e-09, -4.738308e+18, -1.228815e-09, 2.097152e+16, -4.440036e-06, -3.762990e+02, -2.642879e+12, 3.100004e+10, 3.604336e+12, -3.951650e+11, -1.023763e+15, 4.908325e+17, 2.123963e-19, -1.744445e+09, -2.874189e-06, 2.208907e-08, -2.353407e+10, -1.020581e-03, 1.689180e-01, -2.563565e-12, -1.220758e-15, -2.657970e-16, 1.140528e+10, -2.802143e+14, -3.835574e+00]
    @s2.setter
    def s2(self,value):
        pass

    @property
    def i8_1(self):
        return -66
    @i8_1.setter
    def i8_1(self,value):
        if (value!=45): raise Exception()

    @property
    def i8_2(self):
        return [-106, -119, 126, 87, 95, 79, -1, -15, -4, -30, 76, -121, 35, 80, 5, 7, -36, 102, 120, 105, 86, 98, 113, -62, 105, 38, 93, 20, 92, 7, -99, -121, -56, 50, -35, -95, 2, -43, -49, 73, 49, -42, -24, -3, -41, -59, 119, -108, 82, 98, 95, 111, 114, 115, 109, -125, -60, -45, -110, 31, -73, -111, 69, -108, -125, 14, -87, 61, 114, -104, -72, -67, 35, 26, 61, 59, -114, 125, -82, -34, 7, 71, -117, 125, 79, -116, -81, 3, -59, -121, 112, 64, 54, -9, -63, 37, -86, 104, -105, 7, 72, -99, 84, -3, -63, 77, 27, 36, 52, -110, 60, -119, -124, 82, -29, 107, 124, 105, 96, -34, -11, 0, 59, -39, -107, 55, 95, -26, -60, -30, -102, -94, -28, -7, 76, 56, -31, -68, 6, 101, 67, 101, -92, 120, 105, -119, 114, 6, 9, 43, 73, -64, -18, -77, -72, 84, -101, -114, -50, 28, 86, 103, -83, -109, -59, 82, 96, -70, 20, 75, -44, -3, -115, 60, 45, 94, 65, -108, 2, 12, 28, 110, -19, 20, 102, -41, 42, -61, -52, -54, 116, 114, -74, 14, -21, -43, -85, 16, 57, -62, -83, -79, 85, -7, 109, -45, 102, 28, 123, -96, 2, -37, -19, 104, 4, -43, -92, -114, 34, 44, 29, -96, -99, -95, -101, 12, 18, 107, 125, 114, -65, 126, -28, 114, -2, 9, 79, 69, 67, 78, -26, -95, 109, -81, 22, -61, 84, -16, -84, 57, 8, -88, -124, 119, 8, 35, -56, -14, -90, -73, 118, -4, -93, 35, -76, 6, -41, 98, -69, -108, -78, 16, -72, 43, -113, 71, -70, -51, -41, 62, -38, -58, 58, -127, 117, 67, 51, 34, -98, -13, -111, 13, 2, -101, -75, -22, 34, 42, -93, -106, 90, -65, -65, -82, 55, -111, -28, -114, 54, 0, 39, -46, 19, 78, 75, -116, 64, -120, -81, -116, -96, -36, 101, 67, -96, 14, 76, 74, 29, 67, 101, 68, -83, 62, 86, -64, -76, -87, 8, 44, -61, 31, 65, -120, 3, -82, 127, 105, 114, -58, -117, 52, -104, 117, 23, 4, -79, -44, -113, -65, 52, 83, 39, -120, 36, -80, 104, 46, 12, -61, 104, 99, 4, 53, 36, 91, 115, -8, -32, -111, 53, 6, 70, -70, 108, -68, 119, -3, -40, 110, -15, -94, 23, 36, -39, -87, 96, -89, -73, 119, 117, -45, -119, 48, -70, -28, -22, -127, -16, -56, -75, 72, 59, 54, -15, -57, -113, 78, -24, 63, 118, 74, -62, -101, 62, -123, 28, 0, -9, 30, 115, 47, 86, 88, -58, 91, 103, 121, 81, -78, 80, -50, -13, 33, 92, 107, -79, 55, -89, 34, -121, 82, -105, 59, 73, 59, 119, 72, -26, -122, 1, 41, 62, -11, -41, 101, -101, 79, 27, -73, -90, -2, -96, 10, 116, -86, -25, -117, -36, 13, -52, 90, -39, 113, -105, 71, -7, 2, 109, 106, 70, -86, -82, -121, 94, 58, 13, -124, 119, 34, 36, -37, 47, 23, -101, -96, -114, -37, -21, -37, -77, 121, -43, 25, -105, -6, 5, 3, -114, 30, -98, -74, -97, -43, 16, -84, -44, -56, 1, -115, -100, -46, -63, -100, 112, -106, -128, -2, -106, -116, -1, -43, -24, -73, -124, 14, 69, -90, 83, -85, -103, 52, 22, 58, -90, 77, -121, 110, 20, 114, -107, 102, -76, -6, -102, -38, 53, -100, -72, 118, -100, -113, 120, 53, -93, 61, -92, -84, -125, 81, 127, 125, -8, 99, 70, -49, -9, 86, 103, -96, -96, -40, 43, -48, 29, 28, 90, 45, -118, 111, -101, 24, -25, 123, -105, 124, 17, 27, -6, 111, -113, 21, -88, -117, 55, -7, -24, -24, 52, 39, -36, -81, 78, 95, 13, 121, -8, 116, -106, 45, -49, 19, 12, 13, -127, 109, -124, 14, 18, 84, -61, 23, 68, -102, 115, -34, 7, -10, 57, 107, -48, -53, -67, -63, -100, -84, -31, 79, -58, 56, 89, 40, 63, -37, 71, -7, -53, 91, -66, -74, -37, 48, -37, 123, -96, -11, -56, 80, -88, -53, 27, 7, -29, -124, -46, 22, -103, -67, 93, 42, -37, 18, -126, 120, -81, 74, 26, -54, 19, 86, -112, -38, -57, 119, 26, -62, -67, 126, -50, -31, -36, 120, -127, 123, -88, 43, 50, 61, 94, -80, 35, 41, -109, 71, 91, -118, 66, -60, -127, 47, 75, -52, -66, -125, -111, 44, 116, 9, 68, 115, 113, 8, -4, 39, 23, 54, 107, -119, 1, -68, -11, 103, -123, 29, -92, 15, -10, -31, 35, -91, 38, 37, 110, 9, 80, -115, -120, 112, 110, -28, -116, 63, 85, -65, 5, 122, 19, -84, 97, -16, -46, 97, 104, 28, -83, -33, 38, -18, -8, -126, 82, 81, 88, 109, 118, -56, 64, -96, 36, -10, -109, 74, -86, 105, 123, 110, -116, 91, 15, 123, -26, -121, 75, 63, 24, 94, -43, 123, 74, 79, -42, 74, -102, 57, -27, 116, 126, -100, 2, 49, 17, 28, 27, -58, -98, 39, 50, -66, -75, -23, -112, 64, -16, 60, -62, 122, 53, -42, 21, -40, 88, 2, 62, -103, 108, -74, -95, 113, -49, -73, 63, 94, 44, -41, -68, -124, 46, 13, -17, 11, -100, 58, -98, -40, -64, -56, 21, -47, -120, -7, -23, -51, 27, -99, -42, -109, -55, 106, 92, 110, 19, 32, -117, 4, -34, 65, 72, -100, -122, -69, -94, 122, 60, 23, -93, -84, 30, 118, -92, 88, -104, 23, -71, 115, 106, -118, 9, 64, -34, -71, 43, -92, -13, -82, -5, 15, 18, -11, -113, -109, -128, 104, 34, 72, -110, -59, -113, 69, -106, -74, -66, 115, -31, -27, 59, -73, 73, 120, -34, 59, 126, -93, 49, -53, 114, -122, -28, -28, 94, -37, -90, -32, 80, 15, 4, -101, -78]
    @i8_2.setter
    def i8_2(self,value):
        ca(value,[-66, 34, -121, -118, -12, -83, -43, 55, -53, 31, -100, -37, -116, 69, 22, -60, 59, 32, 51, 46, 109, 36, 31, 49, -99, -69, -99, -89, 27, -18, -77, -63, -101, -122, -60, 58, -76, -86, 58, 49, 48, -67, 54, 48, -30, -26, 95, 42, -13, 17, -93, -34, 28, -49, 8, 122, 22, -72, 109, 103, 15, -81, -73, -53, -112, -52, -54, -81, -126, 35, 3, -102, -125, 67, 125, 44, -48, 95, -18, -103, 114, -86, 108, -37, 70, 48, 7, 19, 0, 35, -104, 2, -51, -9, 70, 41, 118, -43, -71, 59, 32, 36, -10, -2, -76, -18, -93, -80, -27, -51, -70, -87, 48, -98, 5, 72, -120, 86, 62, 69, -94, 23, 71, -124, -88, 34, -65, 6, 33, 73, -101, 40, -104, 17, -68, 53, -55, -11, 12, 24, -63, 121, 98, 58, 125, -13, 6, 49, 71, -72, -22, 53, 83, -97, 87, -117, -26, 6, 93, -98, 82, -111, -84, 23, -73, -10, -34, -118, 64, -89, -4, -104, -83, -52, 8, 64, -81, 33, -91, 41, -43, 12, -66, 31, -17, 46, 91, 9, -124, -117, 108, -15, -39, -92, 29, 116, -93, 107, 58, -7, -35, -116, -52, -11, -35, 66, 6, 32, -34, -123, -102, 102, 123, -104, 51, 80, -84, 71, -65, -4, -121, 123, -87, -21, -124, 63, 122, 74, -31, 123, -31, -63, -106, -82, -24, -42, -30, -126, 0, -38, 127, -13, 101, 60, 104, 54, -25, 50, -19, -93, 2, -48, 99, -59, 103, 28, 44, -7, -58, -19, -55, 17, 58, 15, -23, 75, 58, 11, -2, 104, -58, -73, 56, 84, 34, -4, -101, 10, -106, 41, -88, 15, -117, 5, -63, -106, -9, 40, -115, 47, 99, -66, 120, 126, 5, -62, 8, -111, 123, 92, 122, 24, -31, -65, 115, -43, 5, 56, 49, 102, -29, 65, 97, 20, -90, -39, 40, 75, -43, -47, 86, -104, -32, -90, 14, 13, -75, 8, -9, 104, 122, -24, 77, 10, -100, 26, 0, 35, 55, -10, 17, 22, -29, 115, 117, -10, -54, 37, 46, 48, -28, -105, 20, -117, 73, 93, -63, 9, -125, -94, 57, 119, -10, 11, 49, -57, -14, -107, 90, 72, 96, 55, 86, 81, -86, -70, -125, 17, 100, -91, -70, 87, 29, 100, -19, -45, 46, 25, -49, 79, -10, -1, 22, 75, 9, -50, 114, 106, -122, -89, 41, 1, 105, 123, -69, -123, 77, -61, -100, 15, -113, -19, 46, -53, 46, -89, -97, -38, 92, 73, 68, -101, 118, 67, 23, -17, 73, 109, 36, 76, 69, -10, 7, 64, -39, -49, -4, 3, -102, -15, 117, -8, -83, 6, 117, 105, 26, 28, 19, 66, 24, -47, -64, 86, 4, 57, 95, 23, 24, 76, -15, 106, -58, 77, -10, -112, -39, 55, -4, 95, -90, 61, 64, 32, 68, -43, -108, -15, -6, 63, -105, 72, -84, -10, -11, 122, 46, -84, 26, 76, -88, -67, -95, 10, 10, -89, -121, -65, -69, 112, 37, -106, 75, -94, -60, -7, -72, 44, 71, -108, -71, 31, 99, 9, 10, -68, -56, 69, 0, -71, -4, -87, -6, 83, 7, 108, 98, -37, -60, 16, 23, 26, 3, -119, -20, 58, 102, 29, 111, -43, 26, 37, 34, 9, 82, 76, 120, 7, 51, -35, 65, -93, 38, -82, -44, -31, 120, -93, 7, 10, -76, -12, 105, 41, 13, 123, -90, 57, 84, -123, -21, 49, 104, -103, -32, -79])

    @property
    def u8_1(self):
        return 222
    @u8_1.setter
    def u8_1(self,value):
        if (value!=232): raise Exception()

    @property
    def u8_2(self):
        return [20, 34, 154, 240, 82, 27, 230, 242, 253, 161, 17, 124, 80, 120, 210, 237, 179, 95, 224, 104, 74, 77, 148, 17, 98, 7, 13, 203, 155, 197, 223, 36, 207, 87, 56, 56, 76, 112, 100, 154, 40, 239, 13, 185, 77, 91, 107, 73, 196, 234, 3, 235, 40, 222, 224, 46, 47, 150, 167, 104, 206, 245, 20, 181, 133, 190, 255, 1, 183, 218, 5, 121, 233, 68, 72, 140, 250, 213, 199, 143, 41, 22, 238, 149, 235, 42, 170, 2, 58, 242, 91, 116, 62, 167, 113, 28, 8, 0, 199, 142, 8, 102, 60, 87, 147, 104, 125, 163, 135, 1, 186, 44, 117, 103, 186, 50, 68, 179, 203, 61, 231, 80, 45, 35, 231, 127, 93, 49, 154, 182, 1, 151, 111, 70, 127, 13, 41, 113, 170, 41, 173, 14, 129, 108, 235, 166, 153, 50, 203, 42, 43, 93, 243, 114, 190, 225, 12, 227, 24, 221, 177, 188, 218, 55, 6, 199, 162, 67, 152, 185, 216, 108, 251, 225, 146, 85, 220, 192, 36, 39, 20, 189, 24, 117, 98, 107, 215, 238, 145, 113, 40, 184, 110, 186, 66, 207, 164, 43, 70, 242, 211, 65, 232, 92, 164, 178, 3, 120, 1, 28, 247, 234, 210, 20, 61, 83, 147, 174, 177, 131, 229, 117, 211, 161, 73, 161, 224, 80, 219, 151, 131, 42, 37, 46, 68, 213, 62, 101, 8, 143, 146, 103, 52, 69, 7, 241, 55, 191, 104, 208, 100, 192, 48, 199, 30, 38, 148, 25, 252, 47, 18, 152, 142, 181, 231, 205, 166, 171, 14, 236, 15, 232, 235, 36, 66, 88, 141, 87, 66, 9, 94, 214, 100, 227, 207, 1, 6, 102, 170, 53, 53, 152, 136, 115, 251, 227, 218, 164, 20, 109, 174, 36, 135, 122, 237, 146, 226, 42, 202, 183, 112, 68, 121, 92, 23, 75, 34, 228, 131, 141, 52, 12, 132, 12, 43, 220, 33, 110, 30, 120, 244, 192, 128, 190, 89, 109, 165, 9, 25, 27, 129, 135, 80, 17, 217, 152, 237, 241, 56, 233, 78, 224, 115, 143, 214, 201, 78, 139, 50, 185, 115, 234, 31, 11, 190, 244, 28, 93, 13, 153, 78, 154, 62, 86, 40, 133, 29, 12, 133, 69, 50, 197, 127, 242, 14, 173, 70, 116, 243, 200, 197, 245, 249, 231, 139, 46, 99, 37, 55, 220, 57, 103, 163, 71, 252, 54, 52, 254, 97, 158, 155, 249, 243, 55, 112, 226, 88, 25, 29, 41, 109, 6, 219, 193, 89, 193, 164, 166, 103, 119, 69, 214, 105, 14, 20, 208, 56, 231, 59, 68, 49, 107, 119, 99, 109, 210, 234, 228, 111, 219, 32, 211, 172, 101, 172, 99, 227, 112, 137, 204, 19, 3, 111, 219, 245, 89, 106, 32, 108, 234, 81, 72, 27, 99, 151, 212, 108, 37, 248, 183, 241, 194, 37, 73, 230, 130, 11, 6, 122, 220, 192, 114, 116, 208, 187, 159, 226, 98, 191, 253, 226, 39, 212, 138, 106, 196, 153, 61, 218, 218, 20, 238, 82, 237, 196, 114, 135, 239, 221, 20, 52, 73, 208, 234, 99, 185, 218, 218, 47, 95, 218, 110, 165, 216, 121, 249, 203, 206, 213, 201, 138, 253, 43, 238, 131, 62, 229, 123, 69, 175, 61, 176, 180, 72, 120, 158, 91, 145, 16, 162, 70, 54, 170, 170, 60, 9, 226, 40, 66, 159, 139, 83, 20, 171, 32, 189, 140, 122, 1, 64, 144, 250, 94, 74, 91, 160, 146, 146, 17, 78, 43, 115, 166, 63, 81, 88, 83, 178, 177, 110, 93, 188, 29, 41, 28, 73, 40, 245, 49, 63, 134, 103, 135, 17, 172, 150, 249, 23, 230, 166, 31, 55, 203, 149, 19, 4, 101, 237]
    @u8_2.setter
    def u8_2(self,value):
        ca(value,[52, 40, 13, 185, 137, 3, 173, 236, 60, 18, 206, 224, 231, 19, 31, 139, 177, 201, 100, 37, 8, 94, 145, 135, 217, 32, 59, 26, 243, 213, 97, 78, 145, 136, 142, 249, 46, 247, 20, 240, 47, 211, 60, 35, 170, 0, 119, 14, 36, 7, 165, 132, 35, 199, 33, 45, 27, 111, 135, 50, 210, 248, 118, 162, 199, 152, 28, 202, 222, 8, 191, 40, 134, 213, 36, 131, 198, 76, 82, 212, 26, 33, 219, 181, 213, 205, 104, 118, 74, 239, 226, 65, 161, 29, 158, 223, 175, 214, 160, 65, 229, 56, 207, 64, 194, 167, 85, 221, 82, 56, 182, 226, 206, 71, 203, 116, 201, 234, 16, 42, 32, 47, 149, 161, 173, 60, 195, 59, 138, 241, 52, 152, 48, 57, 137, 206, 201, 58, 242, 139, 149, 42, 185, 94, 27, 224, 249, 33, 24, 18, 148, 104, 89, 163, 94, 214, 232, 133, 74, 124, 117, 39, 0, 73, 86, 254, 186, 224, 96, 236, 113, 39, 28, 245, 218, 147, 215, 62, 191, 23, 20, 27, 32, 151, 25, 225, 3, 157, 221, 133, 124, 35, 41, 177, 93, 137, 198, 96, 129, 235, 21, 10, 110, 16, 25, 65, 153, 157, 139, 82, 24, 43, 4, 180, 238, 174, 226, 183, 56, 224, 239, 130, 62, 40, 12, 226, 219, 164, 71, 242, 179, 227, 53, 148, 38, 228, 151, 2, 249, 132, 56, 253, 10, 107, 241, 56, 97, 88, 198, 203, 33, 132, 212, 44, 239, 7, 206, 156, 144, 93, 44, 71, 40, 171, 60, 234, 89, 238, 114, 240, 145, 141, 51, 180, 85, 75, 125, 219, 2, 121, 53, 12, 223, 90, 174, 248, 45, 39, 151, 5, 155, 29, 244, 124, 156, 60, 250, 52, 54, 186, 95, 245, 18, 51, 52, 183, 105, 226, 245, 214, 94, 254, 98, 14, 46, 203, 225, 95, 126, 178, 49, 82, 159, 231, 170, 250, 63, 162, 156, 218, 184, 211, 76, 181, 97, 180, 239, 45, 135, 147, 49, 147, 0, 32, 22, 77, 209, 215, 54, 83, 29, 127, 80, 150, 50, 15, 69, 33, 118, 255, 168, 201, 2, 218, 13, 53, 164, 101, 34, 218, 110, 107, 147, 5, 78, 135, 1, 11, 242, 43, 181, 108, 107, 46, 176, 74, 2, 251, 26, 97, 254, 79, 204, 97, 41, 90, 126, 81, 202, 70, 30, 70, 50, 25, 56, 249, 245, 159, 6, 102, 21, 85, 8, 94, 115, 88, 32, 33, 111, 138, 229, 238, 152, 198, 74, 111, 86, 151, 165, 232, 2, 13, 42, 228, 219, 158, 227, 203, 47, 8, 83, 139, 184, 165, 123, 55, 29, 198, 119, 78, 182, 200, 77, 8, 5, 135, 164, 82, 235, 210, 47, 105, 53, 186, 64, 197, 24, 14, 39, 161, 187, 136, 58, 118, 225, 162, 203, 5, 214, 155, 45, 3, 111, 126, 99, 196, 82, 14, 156, 165, 134, 83, 179, 5, 226, 237, 151, 0, 219, 251, 160, 239, 224, 133, 230, 237, 221, 233, 12, 3, 189, 28, 251, 245, 89, 116, 113, 176, 40, 210, 216, 173, 154, 216, 111, 254, 183, 238, 29, 85, 142, 189, 89, 235, 184, 241, 2, 99, 138, 222, 47, 128, 97, 235, 195, 106, 118, 196, 149, 53, 188, 70, 113, 85, 90, 53, 179, 32, 23, 28, 95, 164, 49, 61, 151, 70, 214, 245, 245, 117, 172, 75, 153, 117, 226, 69, 205, 173, 139, 140, 163, 107, 214, 18, 111, 194, 115, 236, 32, 239, 168, 62, 12, 207, 220, 162, 160, 13, 147, 252, 192, 145, 150, 207, 112, 196, 114, 88, 69, 252, 193, 37, 84, 103, 108, 32, 205, 224, 216, 206, 251, 185, 17, 55, 185, 112, 24, 8, 209, 184, 156, 65, 48, 196, 236, 45, 97, 65, 218, 239, 59, 191, 137, 3, 182, 135, 46, 142, 163, 39, 63, 219, 66, 166, 8, 41, 175, 79, 77, 134, 159, 149, 118, 63, 191, 86, 103, 32, 2, 239, 107, 199, 122, 148, 93, 252, 176, 112, 130, 88, 102, 225, 199, 89, 100, 221, 177, 118, 102, 77, 192, 224, 117, 13, 213, 164, 87, 91, 157, 211, 14, 248, 15, 0, 165, 101, 185, 228, 203, 227, 44, 157, 68, 34])

    @property
    def u8_3(self):
        return numpy.array([23, 5, 170, 52, 174, 242, 108, 186, 30, 27, 38, 181, 184, 103, 240, 129, 69, 179, 148, 194, 57, 7, 19, 111, 244, 86, 238, 36, 31, 44, 193, 106, 229, 159, 23, 70, 184, 121, 243, 215, 187, 115, 89, 141, 233, 105, 150, 224, 245, 251, 44, 148, 149, 123, 141, 9, 77, 17, 146, 157, 112, 122, 83, 50, 156, 178, 186, 244, 234, 165, 6, 223, 148, 48, 189, 46, 209, 30, 203, 186, 4, 159, 162, 97, 97, 232, 113, 178, 244, 172, 54, 52, 252, 32, 35, 131, 178, 21, 131, 165, 203, 113, 141, 3, 195, 54, 143, 163, 15, 99, 29, 235, 125, 45, 50, 157, 255, 7, 81, 221, 70, 225, 119, 220, 98, 55, 213, 23, 219, 152, 148, 113, 89, 236, 109, 187, 7, 80, 140, 226, 71, 34, 17, 176, 15, 30, 239, 251, 10, 64, 170, 150, 245, 180, 83, 242, 138, 154, 226, 193, 119, 43, 85, 164, 187, 73, 19, 81, 119, 168, 160, 222, 100, 230, 27, 237, 43, 71, 144, 132, 212, 131, 241, 195, 181, 175, 41, 115, 149, 128, 238, 212, 134, 110, 224, 149, 217, 213, 122, 200],dtype=numpy.uint8).reshape([10,20],order="F")
    @u8_3.setter
    def u8_3(self,value):
        ca(value.shape,[30, 10])
        ca(value.flatten(order="F"),[66, 135, 166, 109, 89, 156, 182, 63, 217, 36, 212, 158, 7, 212, 235, 154, 155, 52, 234, 220, 30, 251, 223, 77, 163, 204, 220, 63, 152, 39, 193, 217, 212, 4, 248, 69, 117, 164, 83, 149, 60, 44, 96, 78, 166, 212, 56, 87, 183, 20, 0, 32, 244, 16, 155, 4, 82, 217, 235, 203, 171, 188, 222, 15, 0, 109, 97, 135, 62, 185, 103, 39, 200, 198, 50, 190, 246, 161, 102, 32, 246, 11, 26, 132, 145, 141, 15, 112, 193, 105, 130, 61, 177, 104, 39, 164, 188, 131, 6, 9, 222, 109, 161, 211, 254, 73, 117, 59, 96, 146, 92, 148, 175, 82, 108, 215, 210, 4, 7, 176, 191, 129, 174, 224, 139, 166, 71, 30, 57, 246, 94, 139, 121, 190, 210, 181, 44, 71, 7, 118, 76, 223, 173, 181, 88, 138, 18, 146, 233, 135, 205, 101, 92, 222, 136, 177, 15, 167, 154, 198, 194, 185, 166, 21, 49, 193, 229, 153, 231, 101, 47, 40, 181, 138, 207, 168, 73, 19, 108, 15, 22, 193, 101, 151, 216, 153, 20, 140, 209, 15, 117, 246, 86, 210, 193, 254, 56, 41, 223, 107, 179, 130, 220, 46, 248, 200, 241, 173, 67, 147, 93, 87, 108, 13, 180, 112, 58, 210, 243, 94, 113, 140, 172, 53, 206, 186, 106, 167, 48, 43, 213, 157, 135, 243, 72, 173, 185, 62, 188, 162, 61, 19, 156, 215, 24, 216, 222, 56, 211, 151, 178, 251, 238, 47, 51, 141, 109, 214, 179, 41, 5, 190, 79, 27, 13, 208, 37, 97, 178, 83, 150, 77, 187, 179, 12, 73, 156, 167, 167, 106, 198, 157, 133, 80, 183, 15, 1, 204, 84, 250, 122, 232, 178, 103, 225, 110, 97, 23, 171, 88])

    @property
    def i16_1(self):
        return -13428
    @i16_1.setter
    def i16_1(self,value):
        if (value!=2387): raise Exception()

    @property
    def i16_2(self):
        return [-31396, -31525, 21618, 420, -4709, -28067, 13158, 30433, -5226, 177, 32486, -24906, 14134, -12316, 815, 14221, 25078, 4427, -24570, -2404, 32275, 16625, -18211, 8224, 11466, -8053, 25673, -5521, -3629, -28951, 16888, 3476, 29692, -16313, -6124, 7022, 20178, 363, -26079, 6451, 26271, -9454, 7484, 9626, 18076, -32556, 8132, 22992, -22922, 21831, 9586, 30404, -24016, -22082, 17247, -120, 26786, -30338, 6445, 7710, 12192, 1787, 10373, 8221, 9130, -13265, -29233, -30762, 1430, 29737, 1503, 32216, -27766, 25651, 24365, -20157, 18077, -9909, -2427, -14841, -32092, 2606, -29807, 31676, -2674, 21400, -31068, -7881, 15682, -5497, -4695, -7670, -26719, 7180, 31393, 20250, -18099, 12591, 18352, 16854, 24663, -12445, 3967, 13535, -9324, -28110, 13977, -23172, 14216, 30378, 6653, 19203, 7298, -23065, 18301, 27111, -23775, -27934, -4797, 22319, -5834, -10073, 21636, 26423, 20007, -23826, 9433, 24251, 29231, 26264, 2698, -10085, -21536, -27028, -24687, -3768, 1511, 25182, 29258, -17177, 8345, 9571, 7512, -28872, 10123, -10644, -7612, -13232, 24346, -25900, 28049, -5366, -8968, 5589, -21840, 21891, 25327, 9095, 4382, -30532, -21172, -27251, 12320, 30065, -29933, 19371, -5654, 7815, -26289, 12614, 13834, 29357, 25201, -32309, 20042, 16706, 2312, -20975, -5346, 1820, 9166, 20644, -3811, -12569, -3711, 11580, -24719, 29072, -26433, -12475, -15326, 1071, 10750, -17120, 21953, 11265, 3513, 20747, 32085, 9898, -24426, -17231, 21523, -26126, 8783, 31762, 6629, -32554, 28071, 23409, -6423, -25261, -13387, -2606, -23878, 5003, -8970, 16999, -11501, 15402, -31573, -12730, 17823, 3018, 13959, 6305, -24676, -28537, -21613, 15353, -31686, 7264, 14978, -2702, 25179, 16061, -5220, -20419, 17023, -5104, -17836, -24537, 30832, -8236, 20473, 31052, 9467, 25660, -4882, 28392, -16236, 15059, 18409, 2709, 9637, -28754, -28261, 14474, 281, 24844, 25464, 26378, 8331, -8080, -10826, -3874, 21290, 1599, -375, 8436, -25280, 25907, 19361, 6448, -26639, -15164, -12896, 1476, -15877, 23427, -24851, -23147, -11525, 16456, -23417, 31519, -10431, -14222, -28958, 6194, -7802, 17086, -5885, 23977, 29347, 3648, 29674, -27985, 1834, 30677, -30455, 32438, -23495, -10403, 10370, 32713, 27187, -4733, -16686, -21336, 7793, 15123, 17046, 28022, -23346, 21816, 16826, 19747, 21625, 17895, -23683, -142, -27996, 6601, -13889, 24112, -19505, 24425, 11673, -3507, -9946, 20693, -28974, -30639, 25202, -24295, 27916, 5920, 17325, 29121, 12475, -1179, 5379, -21558, -8684, 7551, -8536, 8673, -13435, -3870, -6389, -26193, 13662, -17405, 3305, -15401, -10014, 6645, -9322, -15604, 7511, -8894, -2421, -21984, -12209, 16631, 19022, 11644, -3624, 25297, 6613, 4801, -17413, -12780, -28095, 17986, 11066, 22207, 17717, 3613, 14987, -19860, 12693, -13482, 10471, -24561, 32333, -25968, 7244, 7005, 17820, -18897, 13208, 16753, 32551, 21296, -15046, -3886, -13628, -2550, 16059, 1090, -27901, 21254, 21726, -17180, 5902, 30053, 31909, 25120, 3958, 18119, -25501, -4974, -11464, 24068, 19720, -8793, -9011, -11975, 7025, -15041, 21009, -15123, 3647, -28657, -7700, -10174, -16814, 4848, 13044, -20100, -17977, -29197, 31169, 15459, -27346, -23297, 1639, -27165, 25474, -4981, -16728, 24962, 6895, 16619, 12965, 10990, -13275, 1119, -10243, 10364, 3763, 3565, 31542, -22261, 15267, -31448, 13298, -8408, 511, 19296, 24390, -25118, -29033, 11413, 25520, -23675, -12986, -3952, 7133, 9587, 30652, -21444, 23859, 22577]
    @i16_2.setter
    def i16_2(self,value):
        ca(value,[-29064, 7306, 1457, -19474, -671, 22876, -14357, -18020, -23418, -10298, 1040, -2415, -22890, 4293, 25366, 12606, -31678, -15908, -11164, 20643, -239, -15149, 25272, 17505, 24037, 8264, -3888, -12405, -28698, 25222, -2506, -26405, 9561, 27093, 8022, 23338, -31489, 24117, 18018, 25324, -22192, -23413, -12544, -29675, -10752, -7108, 3021, 29238, -10332, -1818, 23363, 31568, -15057, 9565, 30520, 1064, 26637, -29070, 11149, 8534, -13775, -18359, 9626, 10662, -23713, 28470, 8840, -25279, 18175, 13675, 14955, 30323, 924, -13113, -21483, -6641, 12790, 26367, 27907, -1062, -24249, -13215, -18475, -11121, 2339, -2361, -7790, -26038, -6984, -10142, 8485, 17258, 6150, -25530, 9655, -11378, -805, 11574, 16094, 21091, -11882, 21514, 27655, -27624, -23592, 17985, 3154, -1292, 11059, 27599, -2741, -27514, -27353, -1824, -26419, -19633, 23008, 22184, 25855, -4965, -18710, -6802, 25237, -24262, 3253, -28401, -19864, -11711, -27668, 28671, -1376, -8600, -12691, -18972, -5265, 3901, -6694, 19018, 29612, 8047, -26257, 28662, -6164, 9407, -12556, 1421, 14531, 28000, 8499, 5512, 28989, -17181, -4051, 28130, 19063, 31736, -28399, -4663, 25520, -18490, -32156, -15267, 29245, -13510, 13446, -31039, 18030, 25419, 24594, 28348, 17845, -26123, 20713, 29810, -25881, -10534, 9038, -15614, 20117, 11436, 7078, 9985, -2758, -13790, 12865, -6824, 10924, -4750, 10127, -30953, -15114, -10407, 13061, -13241, 22268, 15514, -23952, -22361, 25465, -23395, -5885, 23643, 6634, 1768, -4390, -29064, -18261, -18954, 22866, -23739, -15996, -31521, -12816, -11246, -16029, 4113, -18809, -4282, -3892, -21196, 23692, 6488, -8949, 28859, 23717, -20358, -4216, 6700, -14565, 14268, -17978, -3865, 21937, 17864, -26293, -9181, 28460, -27725, -32278, -13856, -21763, 10310, -4066, 32078, -8132, -14677, -11698, -23123, -30968, -21889, -2192, 29299, 623, -26725, -29380, -18038, -25037, 26361, 22773, -31157, 22096, 10336, 26530, -74, 3820, 52, -28257, -29110, -29891, -23752, -23846, -15516, -21528, 14792, -4286, 26942, 17922, 21495, 16249, -30305, 3056, -22525, -4198, 28613, 2695, 30388, -18066, -5162, -23655, -25604, -28244, -1196, -6888, 17903, 11721, 13555, 32445, 31800, 11125, -31537, 1400, 25992, 2289, -19330, 29486, -27986, -6690, 9402, 15366, 18268, 29476, 27543, -26894, 28279, -18810, -14493, 6622, 9548, 28691, 30421, -17983, -25525, -6167, 5825, -25283, 19498, -17719, -3858, 8518, 16017, 1325, -16864, 17874, -796, 3678, -32078, -19712, -32173, -25895, 27397, 23474, 10508, -6009, 25388, 17327, 26954, -23909, 27502, -15956, -1770, 1343, -30108, -12923, -3584, -30762, 3386, 18090, -14048, 31833, -5312, -32483, -1358, -28372, -24388, -26718, -17132, 22775, 16924, -8991, -12343, 16874, 19515, 21977, -26287, -28976, -18071, -24572, -8740, 29859, -21779, -20087, -928, 31016, -11442, 16890, -12445, 26140, 23581, -18737, 16033, -16426, -27860, -4853, 6669, -2678, -14760, 15011, 25458, -24354, -4704, 1983, 20655, -3885, -6015, -20382, -6168, -8801, 21318, 21969, 15333, 26667, -15860, -20356, -4265, -19871, -30123, 8082, -5186, -5294, -7119, -23580, 600, 7195, 24630, -9810, -23846, 23416, -26102, 11875, 25362, -17002, 32482, 3733, 8434, 18377, -11770, 21843, -19779, 27194, -16918, -22013, 8387, -1686, -27228, -8013, -12979, 30682, 13008, -32188, 24547, 27126, 12811, -14996, 16305, 16467, 21204, -16620, 20671, 31564, -23123, -31995, 6335, -26234, -8852, -19185, -19636, -15411, 22541, 10295, -14022, -19669, 25371, 4407, -21395, -20754, -31164, -30944, -29004, -28877, 11049, -11492, 30171, -3452, 20020, -30618, 11178, 7734, 15658, 26485, -8697, 24391, 14520, -9994, -11594, 21221, 21327, 22058, -6275, -2272, 20061, 11315, 26569, 21368, 30729, -15573, -25453, -6160, -20236, -29377, -22591, -11045, 19992, -18369, -30261, -32159, 27646, 18350, -6134, 6723, -13437, -23761, -22496, -12447, -1184, -17634, -20936, 30815, 32042, 10621, 17252, 9705, 4169, -8075, -20113, -21095, -20310, -3917, 23438, -1628, 7291, -18739, -12603, 22036, -14198, 26960, -24387, -20204, 1370, -23683, -27522, 31684, -24806, -20567, 606, -14584, -5656, -6025, 20297, -18716, -7075, 21089, -26036, -2747, -18800, 22214, -31288, -31916, -32543, 14577, -6407, 17079, 4683, -29301, -13707, 4296, -2247, -25994, -322, -26904, -4444, 24454, -9676, 29589, 30545, 17995, 20596, 24835, 24545, -15782, 13901, -26644, 4655, -10543, -24521, 30118, -29985, 3163, -27379, 24263, 19271, 12184, 7695, -6249, -26163, -16952, -18930, -22627, 5625, -16862, -29626, 8000, -26542, -21846, 8377, -6837, -30324, 10752, 19676, -31224, -11472, 27419, 4926, -67, 7107, 3149, -18440, 18652, -32124, 26094, -7015, -10179, 3878, 28709, 4453, 20330, -27548, -18729, -7550, -29815, -3110, -14705, -16383, 16020, 15466, 5411, 23434, -14919, -1289, 24403, -2409, -28824, -5982, 21794, -26131, 11683, 28742, -21742, 7952, -9041, 28373, 12434, -17665, -19141, -31576, 650, -11103, -26587, -17144, 20830, 1468, 23981, -6189, -1574, 11151, 9314, 12189, -19801, 23310, 3132, 1145, -5231, 1387, 3230, -15314, -17253, -29867, 22979, -28009, 7686, -31739, -16295, 23702, 9141, 18300, 31485, -11124, -30999, -26289, -32371, 7900, -5057, -8202, -15209, -26424, -2712, -25152, -7174, -25019, -14712, -10703, -2809, -9, -17905, 20882, 31301, 8989, 20139, -235, 707, -23246, 4519, 5621, 9609, -10846, -1873, -17425, 30184, 23010, 18718, 24429, -2168, 23884, -19503, 9419, -24927, -16803, 11872, 16572, -30227, 4356, 18692, 3493, -29119, 16296, 1632, 8736, 7806, -13904, -26360, -27538, 6861, -8093, -6184, -445, -2181, -9581, -2722, 22857, 4100, -2585, -25935, -26353, -21284, 7497, -5385, 10974, -7747, -19865, -1205, -12806, -7505, -29792, 16793, -2743, 30123, 9379, 17381, 4947, -15940, -3652, -1797, 21012, -10333, -27953, -1716, -28455, 29598, 17497, -5363, -3990, -29921, -27210, 8825, 8046, 11062, -13647, 29708, 1335, -22559, -28213, -9634, -17768, 32543, -15641, -18576, -23375, -25305, 11930, 11338, 28057, 12085, -17504, 29366, 3513, 26451, 29229, -24338, 1541, 18497, -8424, 12969, -20692, -24323, 1876, 8233, 10893, -10761, -3855, -21938, -6268, 32120, -25120, 20729, -371, 25746, 28224, -25625, -22924, -30667, 13100, -3160, 28610, 2206, 977, -17607, -2173, 24212, 14451, 22276, 26268, -10890, -23818, 30052, -18695, 14828, -16839, -18543, 17056, -3715, -7372, -16029, 31885, -20617, 10847, -12068, 29898, 12865, 30922, 17546, -8489, 19324, 584, 9798, 2421, -17432, -10905, -14728, -7920, 6909, -11895, 1031, 18387, 20783, -28969, -535, 31095, -30709, 28734, 15322, 28585, 2100, -6234, -28704, -2813, 22201, 16682, -1576, 9351, 30508, -9447, -21309, 3023, -19963, 13739, 8398, -11148, -9348, 32285, -22925, 697, -9683, -1106, 11252, -16321, 31326, -22577, -107, 3355, 22765, -10391, -26902, 10375, -2846, -21378, 2649, 1284, 23016, 6884, -5356, -17352, -9866, -4313, 15950, 12058, -32753, 6124, -9833, 8828, -11711, -28691, -31249, -31354, 13039, 29161, -17382, -5879, -21118, 11736, -29024, -15440, 9364, 28121, 16093, 20123, -26504, 25957, 11858, 9932, -11333, -15770, 3678, -18107, -25852, -21244, 2225, -13899, 2050, -21656, -7352, -3896, 4161, -27416, 12792, -1807, 18088, -9590, 1851, -11661, -28665, 10986, 18137, 22612, -1617, -11139, 19293, 4080, 8597, -16998, 17228, 6587, 12316, 12640, 1001, 25972, 29637, 27715, 5577, -12737])

    @property
    def u16_1(self):
        return 60981
    @u16_1.setter
    def u16_1(self,value):
        if (value!=54732): raise Exception()

    @property
    def u16_2(self):
        return [28720, 34616, 62158, 23483, 4737, 55943, 56769, 39984, 64598, 51111, 51377, 21150, 23557, 7441, 55455, 37627, 34814, 32887, 12525, 7947, 30317, 19555, 62568, 26666, 35231, 38385, 56455, 37676, 47722, 60644, 1037, 61159, 64542, 21655, 57027, 46262, 64919, 49927, 25520, 56784, 4424, 62463, 26885, 43771, 5149, 7537, 28615, 2661, 41921, 63221, 30209, 37930, 9683, 52406, 24968, 50022, 51469, 57731, 65408, 57019, 62539, 10550, 35726, 34413, 46756, 63743, 50854, 1075, 36709, 52737, 38989, 14194, 10541, 39864, 7632, 6335, 37317, 18084, 18417, 13903, 41588, 4410, 55813, 34564, 62937, 56211, 51771, 32961, 36295, 58221, 4107, 18571, 55106, 52625, 36243, 52487, 10236, 36619, 24439, 41204, 61791, 12156, 5380, 26272, 45613, 37851, 60070, 38759, 33502, 2147, 28146, 45977, 51698, 33640, 38956, 48664, 51750, 42329, 6020, 42645, 44393, 47459, 64398, 2683, 18251, 5304, 38780, 13706, 58825, 12565, 37762, 21280, 39402, 56275, 25627, 41371, 39366, 61829, 8892, 26779, 311, 47322, 26823, 8265, 12495, 38802, 20059, 32724, 7618, 37557, 57579, 33492, 20655, 19185, 57872, 51794, 16721, 52071, 52584, 57226, 28584, 9690, 10117, 41708, 38496, 56164, 53099, 45246, 34962, 41133, 9780, 39381, 53780, 14719, 64870, 38034, 15484, 24376, 39802, 58424, 52906, 45995, 50396, 21981, 32813, 15889, 33981, 58999, 48157, 23717, 24644, 18059, 47204, 45872, 26705, 46193, 56697, 41192, 56316, 43920]
    @u16_2.setter
    def u16_2(self,value):
        ca(value,[27153, 43996, 41432, 58304, 12942, 58876, 28186, 11185, 10827, 17769, 13091, 23017, 17671, 49113, 6987, 35547, 2024, 33499, 26956, 11772, 20498, 42863, 65021, 31883, 61940, 6622, 59235, 6137, 51350, 48773, 57425, 56027, 38431, 12927, 54445, 12445, 27087, 33727, 51305, 48371, 7488, 32356, 59057, 10185, 57955, 46571, 326, 43692, 43661, 25990, 42979, 8957, 59425, 9205, 42414, 10752, 5573, 37965, 14726, 60329, 24708, 38900, 13804, 12531, 19400, 40437, 3102, 15384, 9922, 48890, 655, 58588, 55933, 56542, 20001, 11584, 62303, 19888, 38565, 19636, 21974, 26170, 61468, 27655, 30144, 38002, 59044, 33839, 58996, 7516, 41660, 26146, 20606, 9052, 41933, 43479, 45221, 37564, 60731, 9073, 5647, 25184, 21426, 47334, 48473, 57336, 38775, 56475, 55863, 33194, 59184, 17109, 10792, 35915, 37682, 18123, 56383, 55538, 26718, 29128, 5521, 51803, 22632, 19827, 32242, 38280, 51359, 10800, 22661, 63621, 58920, 22073, 59845, 56670, 24860, 21801, 22225, 45849, 35453, 38351, 58831, 63677, 49340, 58625, 59284, 8244, 22567, 42599, 39629, 44023, 55480, 23933, 54557, 36080, 18074, 53598, 26233, 46291, 10356, 982, 20899, 9791, 43246, 40308, 38630, 40376, 23805, 35194, 45957, 56662, 38493, 50650, 41811, 40225, 20212, 10975, 38947, 14443, 62213, 16366, 55641, 20063, 28304, 34336, 48695, 11196, 20382, 32670, 61020, 27154, 60750, 42124, 64065, 45687, 32335, 60310, 14344, 39059, 31190, 12119, 57101, 13774, 58824, 54012, 32689, 12347, 13368, 42262, 15453, 61631, 51804, 27658, 53000, 30414, 42427, 61957, 16811, 19230, 23527, 24728, 60773, 28925])

    @property
    def i32_1(self):
        return 898734
    @i32_1.setter
    def i32_1(self,value):
        if (value != -9837284): raise Exception()

    @property
    def i32_2(self):
        return [-461364931, -881174363, 1190512124, -652344200, -1904465790, 654215830, -8237446, 1554134258, -1171405181, -2097329372, -1168547037, 4964041, -162499187, -1566779923, 396658647, 1372847452, 1952977117, -2055030887, 1369558008, 1159869637, -151488968, -1230916956, -1662654082, -692556634, -2108882739, 1919783279, 86726599, -479175753, 368307099, 263085896, -1297854452, -475865862, -1052798892, -195216089, -1808717864, 1435851230, 213845163, -2014435943, 1958739019, 1950538379, 195043354, -2094251280, -552928187, 212026163, 1882789473, -1701156512, 700729029, 617009319, -51379635, 1437981860, 143582562, 1759700160, -1043283958, 790685144, 1053455552, 888961142, 1884764193, -574487120, 205387093, 1706716858, -1564706331, -1119162850, -320357115, -216356729, 1133115157, -1585595150, 1163420546, 2095530513, 959051309, 1266503031, -1940662617, -1207768369, 2071048923, -247500208, 729695364, 1732441574, 919515230, -1307758899, -1362232635, -985845056, 1183002178, -967666429, 61839483, -797969544, 1019207261, -2080745651, -1493399698, 448039065, -1006260032, 547484182, -433873666, -145482008, 1266128764, -374269118, -148627528, -481205875, 28560825, 1620567461, 160877005, -152736921, 566726869, 1690610724, 1551218429, 129384906, 1756514951, -1619123979, -1635458102, 461420293, -1025697720, 1074881682, -1342853402, -2024581138, -1021476707, -979756855, -2061951658, 495595484, 1072057242, -1075816975, 634930689, 1462757877, -355459145, 113806554, -1586994022, -1759236007, 1642313755, 1844726616, 263774839, 865591847, 1137711548, 568540382, 1697402204, 1287333602, -18557107, -543522023, -747044673, -894978937, -1633590316, 1469569043, -1916659051, -245350462, 558791729, -1069756095, -1671183103, -675709621, -1496240619, 1002596182, -1049603233, 1067628357, -320684962, -1756926613, -1978637534, 2115134917, 293851213, 188870457, -2033713174, 316694162, -1680926305, 1578104820, 2019431451, 1672278268, 518272185, -366138444, 1261822504, 1003789835, -595796762, -1764183978, -1066900678, 1415600408, -173332206, 341584118, 1836086928, -77555270, -1989963843, 428500682, -489840295, -1096671034, -1915424250, -1746745758, 473428620, 1155878488, 1534484342, 1866809635, 2125417205, -356683367, -724519561, 476765866, -509611460, 1067343485, -1663160103, -1973204454, 1891962125, -1486851183, 539703058, -78175960, -1038870474, 585234261, -1015599511, -1860840029, -1939494917, 2120890829, -1396051426, 442584714, -559475888, 1852553473, 1370937853, -189979498, -1942748392, 575014321, -206759426, -31154557, -2070305927, -1863241823, 976830155, 405210820, -1810403626, 1246769487, -1690543149, 1313271912, -351123144, -169833423, 329135592, 1471013659, 1018659812, -1227714342, -191860948, -1335651686, 883360682, 836140176, 533570354, -306737045, 503171813, 1574245195, 486740175, 2103577114, 1369514515, 631086314, -1519000748, -1651625120, 2072505877, 343400009, 1919137338, 1103988337, 2071554186, 150773570, 2097705645, -130202734, 327475069, -884235865, 52111222, -1080547500, 682409781, 1559839293, -1958998234, -668500619, 1652828958, 1898194722, 1411170984, 2027809940, 2057915321, 624976316, -1590230095, -39277437, -399063086, -199887533, 1695889089, -179411470, -814891514, 441001215, 228328910, 1969824685, 1673102538, -939256124, -2021849575, 1292458519, 1963232860, -701199322, 1898059105, -2045458245, -896773856, -465102206, -1132267068, 1715928377, -1576771507, -76241412, 1187144803, -1067322651, 570283207, 1328683328, 1679817753, 1351131251, 218112167, 1288274663, 1769551475, -1459879021, 907399627, -129113618, -816814174, -281922806, 1308242407, 959061391, -643658909, -1586885260, -731576338, 872407494, -1435528398, -978470065, 561011867, 2094464646, -1961457104, -370593344, 173444003, -1787659154, 1403917210, 1314481998, -2064760703, 627159779, -1209896425, 950681678, -1599356229, 1797678336, 1407713282, -1860763990, 1818135625, -797982794, 1766490463, 146950743, -573489171, 541336457, -786031692, -823206893, 472702619, 301835709, 903962039, 334036788, 1308489144, 1982571588, -1297489003, 1027291239, -1050223998, 1301065587, -131811840, 840706119, 151612697, -1514662009, 2045477247, -78244632, 1428738052, 999845946, 632205998, -2084777797, -1263080892, -1527740973, -1052672864, -1148385231, 2118437588, 64244951, 610247700, -192213951, -1677840790, 695619117, 194487568, -1064818224, 567953693, -556351633, -358984117, -543035561, 1299534234, -1814192015, -1987974286, -251589327, -1550216573, 1039391427, -648231381, 209808513, -1809205905, 425289643, -1478441699, -499830484, 895438284, 1388891777, -141187536, -1921173432, -2109700894, -629643543, -1992180854, 1262181466, -1000112113, 1891981448, -511356474, 678112000, 231308715, -845426086, 2065931343, -690231821, -2065441467, -497137258, -288817447, -272642500, -1778307241, -206926623, -1058833162, 1207480823, -577760388, 967667904, -747757357, 1515713516, 1901169583, -43384102, -1869097267, 698722931, 1723948263, 895747277, -963077288, 2007160291, -1139652897, -1941673179, 1182316407, -1504345279, -69517474, -1337091986, 1144745436, -295343637, -368530206, 423117467, -1160707313, 606107242, 973575490, 782358427, 1225701496, 1354180679, -1819084457, 210496900, -1607248517, -100403486, 357128435, -1211000784, -1699635523, -1995757335, -2041727997, 1639346630, -1140917407, -1428441321, 1391552530, 950439976, 1536850187, 1755763383, 349315024, -1716747422, 1788059719, -956787148, 435093165, -519717781, -1185043774, 1326150846, 666841562, 977518902, -1878116663, -1052216208, -159814671, 545626237, -1161390691, 172913262, -1143147285, -711220581, -2073758388, 1347605160, -274461216, -1138600943, 1812589913, 1321776791, -654185814, -514865093, 342576025, -1227661029, 2027182643, 499090278, -1057042386, -1200362684, 1633068952, 1127338030, 66338457, 1655244407, 1091076049, 1868857534, 1902975017, 427968982, -689633450, 1869590905, 828919724, 374348665, 291496172, 369492724, -1956000730, 149774736, -283502913, 542857976, 1810830261, 1711344293, -1158072113, -1788295198, -314318981, -1029216204, 1180472328, -769273193, -1884508206, -1558495607, 19086583, 2059341589, -1133755497, -2103950715, -353373479, -330597102, 146329926, 1139012057, -1595155154, 92242787, 1758776536, -2142059846, -1016391823, 572794885, -1164070685, 936895954, -530252487, -852015578, -1387262267, -610552571, 993685216, -2060482368, -54855358, -1368415548, 1727532083, -1998919251, 1004938093, -193604754, 402127614, 15533913, -822374248, 914869992, -398825428, -1951818825, 1024562104, -1513050369, -1086194365, -1602294388, 506250848, -450950473, -1107350963, 724811630, 1667267553, -1296578611, 1797492484, 1593191271, -797438732, -1327763127, 1815794923, 968830944, -1597687229, 453031735, -311267208, -1363949093, -680526092, 2111164100, 1874373703, -737231277, -1941054345, -1943683241, 299275156, -777764717, -1580845667, -1590831315, -706883071, 1006664100, -455650726, 405499155, -1557738572, 1434435376, -476662082, -390599384, -1023097080, -462139722, 1416922513, -1243778374, 1721356353, 2052478481, 1576465185, -1753145409, -1866886190, -709091910, 1188370346, -47903041, 833750418, -714362080, -1356224125, -1264932342, -2019192812, -1865286029, -872940604, -1103730145, 960420100, -1042876502, -1376735106, 652488617, 265536834, -727122450, -1304252301, 1452309463, -345462904, -1385578434, 1005791488, -1952157450, 1535232809, 1539175065, 1764693654, 370125766, -1202518768, -1045824063, -1277351352, -209760871, 745809202, -969253860, -263968717, -1987049520, -994220477, 1014895379, 767424874, -1455749768, -1031331847, 102844430, -1853475234, 1375464119, -36893052, 738438714, -2023227099, -766955665, 917641510, 2098209786, -1217824087, 1658975849, 519874226, -253260859, -1162718483, 1786747123, -1141951794, -2107503630, 454499128, -1967565552, -1023321135, -1996284503, -752431392, 472701630, -1632851902, 410108660, -1046454863, 1967316776, 855860213, -1312902400, 2040315518, -1117439624, 493239897, -1998091182, -2034474271, -1097999735, 1318127173, 606300235, 1842233668, 575662433, -2004034017, -453132858, 575442626, 312602259, -2052800210, 1864640938, -1558226144, 1723181891, 1563560258, 1335087794, 1484455993, 1617896015, -1725417335, 1319720221, -1761963217, -699139792, -1289651408, -1107156983, 1743906484, -4909723, -1308860494, -1458950358, -1346838156, 770842123, -2015270071, -24732450, 1317412484, 713576473, -367369916, 1304052776, 249082034, -1501300599, 440635569, -1918514505, 1703744454, 1979510875, -1459719502, 2080733946, 1591601168, -1279512428, 1050916259, 506633589, 985141457, -1785288990, -264273336, -929708322, -719186799, 821741784, -672362448, 552181928, -802373915, -390543422, -343050866, -1958288614, 898584575, -2009826787, 695541207, -490634204, 1677702760, -881113644, 949838036, -1754707531, 1625802700, -2116565724, 1986923158, 755539119, -1478875610, 266787239, 1794560040, 1005034935, 1558408357, 763790383, 677517420, 2072139195, -235728628, 1725705385, -1582053707, 1113461586, 1674642759, -1414719663, -608468252, -1873260761, -1401304493, -1029303396, 1873534265, 912963743, 645715337, 1132031991, 487696799, 1110621999, 1383752223, 1018103642, 536280867, 1764666589, 1624759145, -707782673, 1407012132, 1887436609, 568473975, -758524638, 1093808445, 330404853, 240981075, -250484760, 498674002, -1126343191, -1070540555, -17257403, -1302522037, -1500566183, -706742387, 1731391627, -121892623, 1944180, 697150366, 1175869801, -1081726694, -772936078, 300113930, -1519743318, 1011619084, 966435032, -271530967, 1478437384, -2000885569, -1625488897, -30409891, -577640443, -491669659, 1721990364, 464531779, -1035520457, 1234811766, 58268492, 761680308, 338102126, -1281454585, 1554633851, -2008859178, 55616722, -2039496630, -902950403, 673529549, 1020509295, 1518665847, -478044459, -296723364, -2075845731, 1809506854, -99500436, 883142933, 289332182, 738556337, 1501633470, 2058318873, -346819242]
    @i32_2.setter
    def i32_2(self,value):
        ca(value,[-966485083, 547919123, -1194190604, 1550099195, -86896479, -1346998266, -111775936, 1595883280, 95277373, -483593724, -1194231658, -1664247993, -1125879490, -774112094, -908971354, 1257430739, 278831106, 2146175077, 1216734947, 108534888, 712376825, 472415212, -413092215, -186896831, -983274891, -814159203, 491332674, -1080086896, 305863740, -588641755, -1173634854, 1500595228, -1011735210, 1396816521, -1843412764, -1174697157, -2042333138, 1720132956, 1179474025, -734588992, 1928960553, 653905969, -1152761709, 206317133, 1066603916, 1788908206, 1901091544, 1610435338, -1051581785, -1953636422, 1076388567, 1462395490, -237116033, 454691362, 1619801391, 1845599647, 1868321380, 1723200218, 766619638, 105371815, -877177590, -1885723170, 434710859, -1146593520, 209995917, -1047842747, 465673729, -2084508649, 1968279245, 587205365, 1583233886, -1752333729, -114021301, 59161723, 1580036234, 345745650, -468378351, 245003371, 1673787261, 1587452615, -1303597866, 822157520, 64527339, -4281296, -64380840, 37142322, 500059241, -1469346913, 11916922, -338760031, -2025817128, 83726551, -754215578, 368103720, -821582629, 717962460, 2144471201, 223671109, -199755353, -841621639, 1540857720, 1804628518, 2118963299, -1595232224, 400238135, 933224750, -215585205, -985264044, -988901458, 986847698, -1856650438, -651146661, -978168494, -532172509, 1691932093, 1876106029, 525396768, 1743090554, -162073951, 806798458, -1403694340, 559542160, 207806919, 590536881, -1650417281, 1858408059, 1983218923, -1543131382, 1706115652, 2119926306, 1424134413, 1205448675, 1811525641, 861875958, 2007619106, -845489490, -55633190, 1816674890, -614507920, 286578932, -1342898663, -1261324825, -1506404786, -1806499804, 1974771054, -98303714, -290587554, 1090231453, -985937256, -839357172, -1416681172, -1007624128, -1578990962, -1728169897, -844916635, 506302833, 667662716, -663874058, -1362455403, -2060230793, -1319792032, -2017894569, -1689519196, 479605380, -117340189, -1052087080, 1498560347, -870303564, 1098382715, -2086046098, -1642542296, -628648039, -719920250, -2060321401, 525438216, 281529006, -459505556, -1796557506, 1024549346, 1853853925, -312303325, -1579857332, -1269984071, 473304768, 721731410, -1737559733, -438494623, 1802127802, -1731233704, -1390726345, 485787940, 943002107, -187237495, 1869312126, 442020547, -87826467, -696183927, 616713843, 945472556, -972856985, 151686386, 1488133092, 175341883, -1180397098, 948926458, -503479659, -1267580010, -388943415, -1363469783, -1527776457, 268299441, 191219066, -1024035842, -1475980660, 1828759673, -1442955646, 1790351422, 574018056, 1803848768, -2095818881, 1210053959, 1551296999, -942626269, -1321443296, -1859662526, -2071020753, -1184904851, 988848078, -412054768, 1493935320, -196557049, -704875093, 134497249, -1224190928, -2068208534, -965095455, -564081208, -1156543555, 461090533, 701882132, 910649700, -1878641070, 1446533896, 1970740772, -204663013, -1698033554, 972688594, 1110078968, 810548960, -1509538061, 1958800693, -543420990, 217640235, 1880493927, -1671735529, 1137613142, 2072545208, -414851757, -1785997391, -364718164, 450315208, -993471993, 768175939, -1566579292, 85961510, -1827000830, -1893503205, 869202084, 713571555, 680257288, 1524440291, 1741022434, 561415328, 1990319608, 1142451744, 39401847, 1221297801, -2124038766, 1215377498, -2068455826, 560063055, 383922313, 7329552, -1417241590, 1973186515, 358937975, 1808732034, 894888594, -1620703934, -1409454021, -224706429, 631015427, -701827114, -1980442971, -1243431585, 1865483925, -1340041763, 259984294, -1443453841, -885229413, 973067512, 780961235, -282514052, -1110338800, -722213025, 1714985605, -1287879595, 1509400751, 324286798, 1011968175, 1774625427, -335835050, 1241953488, -485251005, -2023480468, -1498664236, -1676758135, -2078759270, 368391173, 1770332091, 602035732, -1157125163, -726848951, -296396612, -418101410, 1516209091, -433026570, 2065899179, 286245383, -1428168800, 310716072, -563791242, -1325785953, 1826452534, -23905747, 1034013849, -1085065618, 1611085765, -60799609, 1082236453, 561831452, -1827984069, -277941810, -2097393299, 1609593516, -1947366285, 2039786925, -2039232768, 986451997, 2119304777, 49748214, -1530450382, -588012225, -142349556, 1234615466, -1482467714, 728929313, 438851997, -424861037, -1835013005, -674124377, -1634348548, 1081331853, 2111035427, 143997944, -1158230701, 4815417, 2122369877, -77009634, 282329472, 2124624001, 1395262123, -602351149, 1496495731, -522090375, -1089014497, 1060099030, -514142834, 624755360, 101709947, -259648574, -1721466978, -1470128315, 1344990842, -2138737258, 101466176, 1692425055, -1157926775, 592741389, 1813083585, -769169250, 1770253928, 1208684737, -702112980, 1001273019, 1705993099, 1407346099, -2142523547, -1355363485, -267899641, 449328343, -987691219, 438101969, 572223309, 379113218, 1466899667, -623010689, 2125548615, -145443483, 631502783, 1728343290, 1277749965, 1997442958, -1429886186, -537022197, 763891225, -1238739363, -821719020, 940172257, 114964281, 2090254185, -966856290, 1594918376, -1912990965, 1325705675, 1909184548, 837435170, -590257590, 1748272543, 65934393, 2073600222, 170572472, -1901011521, 2133543824, -1551997487, 1825478098, -941111977, 2081346119, 1276024247, -1737235139, 1172151357, 1861822828, 2017860579, 2079359170, -712881259, 353483674, 1081877284, -310138121, -1387900910, 1509477224, 321767828, -334162604, -1426416668, 122601289, 900426562, -1974038173, -187934215, 1716122553, 536633084, 653559614, -106459236, 612788932, -426096009, -407044580, -231495552, -20598604, -1049988598, 1707164387, -907341708, 1018148334, 420273830, -717817139, 746522674, -1091234728, -769304365, -1783917863, -1773360712, 1421244394, -1489877988, -1400774353, 704671809, -523850319, 107160908, 2024605373, -799692707, -2092464355, -948361722, -1132761744, 429369122, -76789764, -1551036156, -1351725409, -11045966, -1316255914, 1121595316, 1364255025, 1812124631, -1134809617, -1230048918, -1823006270, 103013418, -1985924618, 1276352832, 1604221273, -237209206, -1822616069, -1899068745, 1297703890, -240045011, 810578223, -1422419765, -1418704599, 1034032605, 2085440174, 607645733, 716362365, 1235513555, -1211579413, -261155896, 2022908495, -146539076, 1167671484, -211945140, -268072629, 40741212, -317939085, 728869511, 1342184697, -522128634, -716993901, -885638830, -1889540956, -518758183, 194076888, -263047735, -53295197, -2039369321, -1402107402, -1232069700, -860885703, 667080371, 2003791013, -1792537425, 593890515, -302918528, -371191726, 915728277, 1775934623, -1884658077, 1983888460, 298800478, 1016157169, -1717781878, -1076292572, 1732073196, 542964773, -773239025, 1070547456, 1719362726, -1490080193, -1399780184, -58541011, -1591258, -1250990694, -443129975, 1822357515, -1774941626, -1423917059, -1324183435, 1247654078, -785941226, 208759350, 1371670412, 1903510098, 2128083745, 435649658, 1127890999, -1861063799, -188564302, 1199643492, 1891452416, -217657738, -67141750, -1266789415, 2131626424, 2098938511, 1874390421, -1698831352, 1922731129, 1143118810, -2026197630, 2086052126, 842500141, 287962959, 850955114, 2012362088, -817258418, -1072214227, 978057684, 992062798, -2041866817, -1611489850, 1663409654, 112766564, -1689406122, 1616786320, 556057860, -1680102493, 867719167, 453575899, -191805706, 1712061526, -744377824, -615870979, -1980362202, 1649307499, -613527529, -514007552, -354868527, 740361284, 1191787483, 1421727561, 1066283904, -452434665, 2020141000, -1987374530, 412400833, -621803967, 20900810, 559102704, -443346658, -768206607, 1402289809, -1479041896, 1359182666, 84692384, 1919671125, 1665432592, -1427511811, 1351138729, 714150331, 1584608034, 1063897075, -470363603, 1537682572, 760337828, 270984358, -1339485809, 467876006, 1515737109, -2141726672, 1046916347, 1259950801, -835983188, -2073384503, -697440699, 1343223043, -1288734811, 27645887, -1066885181, 2063044057, -56607701, 319902811, 960858771, -423030408, -812161836, -1112301146, 132484238, 1783289397, -2018957458, 450584409, 1012115988, -2101400823, 1667035362, 1107203875, -1865977929, -723361763, -1343871789, 1135679266, -1675492453, -140706303, 1364740541, -1551211173, -2009393394, 2000971427, -344052593, 462623413, 143090848, -1640955654, 1157518396, 659813664, -165571783, -761091080, 1439584252, -52830785, -1885945630, 1884406245, -555522218, 1323853722, 930747959, 137706091, 555548831, -1337759477, -1009674506, -1977870785, 1180081172, -687421630, 194151065, 1311924712, -866937125, -137781558, -698706859, -1895205467, -1848499551, 1896490516, -6509636, 1269553250, 186532024, -955818569, 1845517066, -400727025, 1078611153, 863814973, -1229137047, 1718754324, -216510561, 1988750453, 29465919, 1428890551, -62281515, -937668540, -1508270436, -927907488, -505451885, 1033857489, -389957828, -2065486196, -352295525, -2105963968, 1299134698, 816779483, 156423679, -1354381381, 1887465750, -2105822745, 642600242, 1123616314, 188710252, -1703216607, 1459661161, -1941560289, 601336479, 1863482085, -857985266, 794305967, -1660447453, 226783646, 241199673, 583367867, 849630317, 1914170489, 565711020, -1488638620, 609086194, 1720536967, -1694564352, 692492707, -1506800749, 730802235, -157471351, 242744029, -164780657, 554729192, 826406260, 2052603794, 1509424364, 880799424, -742089480, -1122708577, 1850636033, 1672099719, 1908731732, 1738334895, -2040611202, 1682998097, 1398609974, -1324949149, -975919403, -1450888087, 1833224637, -619514125, -990582005, 1412067944, 886169183, -391523199, 607372595, -1262130460, -1519841199, -1773159746, -1708684329, 1508540061, -445129927, -861216001, 449901651, 1557438209, -1188736704, -630147206, -679376511, 1198115538, -382787307, 697875997, -22939436, 239787497, 500731101, 195546534, 1392914720, -187209041, 455847608, -2049957759, 766204445, 1368826958, -2042625013, -180992444, -713812831, -114800611, -607409323, 162793232, 2138008530, -1531267188, 868044052, -1630059848, 1621859247, -1597211643, -1129166747, -1199701638, 1770783044, 36166445, 1439401965, -994866018, -960772827, 2001685784, 441293150, 408861924, 905891633, 1537313206, 400637893, 61265814, 1571963795, 838433145, 2065601099, 778646834, 316955585, -2087195141, -1175880744, -1556081321, 1057881099, 261925029, 1208410025, -1666750702, -1564870443, -1780046839, -921180273, 1249930686, 22741986, 1111587522, 1806539596, -2004101869, -1217186294, 1838807150, 1025186692, 1739799205, -970775152, 1248070355, -507661275, 1255915477, 227039459, -1806354804, -1933273622, -1702447540, 998405321, 1478470466, -1376315847, 30712562, -2027352328, -1528293401, -1983304959, 504320567, 1291680060, -1444744047, -1127727805, 1549237293, 1204875828, -290551371, 1890491263, -60192594, -338589164, 520299155, -1570639410, 1365342605, 717971876, 2100041137, 950014485, 2111827591, -1614588413, 1565446784, -711540009, -612602607, -1878381653, 759406734, -1354242425, 1036377793, 283764256, -147639272, -280351513, -314754805, -993828539, 998353033, -1202064568, -1057618001, -395391049, 1549721165, -598972723, -982907535, 1557165381, 1891640427, 654353458, 1775642645, 935383528, -1688413182, -419838142, -1817002350, 1500587707, 439484714, -671255505, -1446765092, 1379929086, 284924340, 322973021, 517663367, 1269409562, 1635098653, -456602725, 216521789, -390880857, 22702718, -141949792])

    @property
    def u32_1(self):
        return 547919123
    @u32_1.setter
    def u32_1(self,value):
        if (value!=1550099195): raise Exception()

    @property
    def u32_2(self):
        return [4251946440, 3334867394, 1627635129, 2588419147, 4174027116, 3897125158, 80443814, 1389733726, 4117149812, 12542280, 1256007817, 1703348194, 4237384057, 1454512978, 2775061970, 3298540861, 3715621276, 2362002640, 3636980763, 3430743390, 1830381203, 1507092396, 4142499824, 4213673901, 1183960426, 1874370435, 4181283334, 2200901254, 3332790298, 3423644529, 2387935836, 952382132, 3924524172, 3719680299, 853249098, 4083610173, 2636543308, 657361882, 1525744446, 376298547, 2451684942, 3240929540, 2310416762, 730671377, 2937427586, 3563592349, 2472196520, 2147357762, 914655107, 1758244054, 3876886042, 12351564, 1679162795, 1489623257, 2455794558, 2538372341, 2057637059, 3508778762, 567682489, 283434754, 3167627543, 1915532592, 1232942381, 2754609078, 4150346060, 1663219004, 1231896519, 2755959635, 183820585, 1055352125, 2147188623, 1645909010, 1893712235, 1485051038, 870164520, 1966826561, 48501444, 2556720793, 3128066451, 790988700, 865202135, 4263049716, 2090861867, 1748977625, 2699841095, 113797990, 2481195137, 2574284167, 834141103, 476065944, 1480757910, 315080683, 350708905, 338916974, 709575589, 3077697353, 1231129412, 746021816, 2332229547, 1946675456, 583346238, 3135681244, 1842291655, 231618544, 104978643, 4086067348, 3174792638, 1543369889, 1101673653, 3023672083, 3205010661, 1536466390, 966572661, 3883854770, 3427219648, 2247096744, 4079126348, 776176295, 2599372279, 1888032134, 360725842, 3052443662, 865793013, 3084628677, 516162558, 1020425629, 2915535067, 4215116317, 2977464272, 1660722837, 3507058298, 864890045, 249379031, 3973345746, 2629825645, 771115239, 3526813236, 3106614042, 203525488, 2971666751, 2845337507, 1637317812, 1743782319, 3991795965, 3057486763, 2839184028, 2831552101, 2836007599, 14115933, 2147447119, 3904004068, 3346997713, 1322155226, 1049159718, 2520132354, 2765453431, 4205328777, 4063219623, 2238279021, 1619016803, 415896490, 3591765870, 3318597287, 1557289292, 2845067684, 89482247, 2114516871, 3464828768, 1114311788, 4215401081, 3458358731, 2736518275, 380431203, 3435888629, 4249714953, 1764633576, 1915821483, 1597234883, 111251916, 274107180, 2935452271, 4072034355, 357724805, 1550422867, 1378849275, 3264188640, 3028697235, 2805673388, 656257910, 1454961285, 188865944, 1924561757, 3184772136, 129725152, 1587697966, 106462817, 1587951867, 3192757556, 2829152265, 3270745049, 435873692, 3749929242, 2062096658, 4149869860, 2418404390, 3646774382, 343128996, 2496743364, 734565947, 3826051517, 2828517029, 962692901, 730853036, 1082602175, 298823790, 3231844899, 526460170, 2579457360, 1480606553, 1842946907, 2622701868, 3895551897, 2026981125, 3153668454, 3704749050, 1185971623, 2504477989, 1870109318, 1518600621, 14687749, 3846239097, 2613355571, 4011868731, 4273118207, 539188665, 2099254272, 1043640546, 2517454961, 4147146631, 3753370580, 3811721724, 989962603, 2211483632, 1480428764, 1954557704, 1112461942, 1569266181, 1678583802, 1646459706, 316406457, 3242999591, 3888012390, 2402113654, 746240298, 3662473135, 1260156363, 1203238376, 3061859356, 2032152659, 966717679, 2534194659, 3388402620, 3223059378, 3877902454, 2566178070, 4108564664, 2578614366, 2924743698, 3967226306, 1346866215, 4129141259, 2159606690, 237374413, 2311773278, 2936435723, 1669343609, 3835118141, 2474006294, 2312776854, 3991958455, 66050323, 2021998927, 3191454066, 2189188580, 2142686591, 262029985, 1334540897, 877178233, 322292574, 583880104, 994626866, 2643853709, 2746736170, 1819097952, 3500683162, 2717819610, 1979841756, 4158317627, 3768907483, 4144867490, 2428342768, 407254584, 3876466370, 2906963449, 2747730439, 2807429483, 390805623, 1347724002, 3708124771, 1996426487, 209852741, 3539291907, 1973958470, 930781564, 3333035683, 555854849, 540149787, 3214341438, 1165683130, 284698251, 3229514555, 1944044250, 676799831, 3415601775, 686883721, 2475380401, 2417075124, 1731220395, 2692854334, 2090593377, 2377595670, 3031508806, 24480902, 3556421449, 1940400454, 3751271557, 585927728, 2399018121, 1897248871, 4110307692, 1294121928, 2976700231, 2519149970, 2393660481, 1452332020, 1320620207, 2261085851, 2445477360, 3141380218, 1044718590, 50521930, 112491419, 4149332237, 1091423792, 1469962572, 3907732209, 3328879500, 4063642960, 3006889620, 425720040, 2842213341, 2094386140, 3171166176, 757382335, 2515418722, 2466505128, 4181749776, 3386253778, 1241141486, 3110299582, 599382492, 3361936057, 2904521896, 3463235864, 1686895148, 4096837571, 2649784396, 102145162, 4034413105, 1309891308, 1727749117, 4111125789, 3485689078, 1298526747, 3208723720, 1387080573, 3497204630, 2701756222, 866112144, 3332181807, 2824696606, 4019789661, 1393196838, 477838543, 3838343203, 2399752805, 1676970714, 2163423971, 3918831727, 2082667742, 687058482, 4132123776, 2944329588, 830337633, 3305684867, 1115400173, 1409924819, 4213431551, 101974285, 721035281, 418956469, 3537419424, 3058980494, 3735712173, 31898322, 812527641, 1412975070, 214035881, 3370497326, 275023508, 2188096928, 2698269714, 2338536560, 2217867267, 780724394, 168999967, 4028242661, 2057116599, 248770288, 142100118, 558526929, 367796080, 1613088719, 111252491, 569035372, 2444968023, 4163888313, 3008206018, 655301551, 1102089047, 2157711351, 1189565715, 1048858627, 3463105328, 1659606364, 2839652561, 311401265, 297227948, 2049718821, 1287086069, 2816817582, 753298510, 79123064, 2058422267, 1988231070, 1697021200, 3755875481, 2000787653, 372680790, 770642272, 3557979977, 3242763045, 3424268849, 2545039983, 3403101537, 804431778, 3022051943, 1799982329, 835187866, 1307679719, 795446639, 2865087004, 2503099400, 1097854687, 412079412, 2918593238, 4204336449, 3272876881, 3701287131, 215671154, 2729194459, 3828900376, 407889473, 2386020434, 1672155598, 1588439879, 2355888880, 2451706408, 2223568426, 4230924842, 1121564168, 3971399371, 2302823247, 1838239260, 4017581704, 197226193, 1773201901, 22730505, 599013585, 2360399780, 3459055993, 2359729316, 2534122212, 3338162386, 681551474, 804682591, 3684776026, 2611917837, 518924291, 3527933723, 2831363989, 2092857661, 3011292035, 2036768662, 1165948954, 3915111934, 3715091842, 3486642823, 2169348932, 2210412086, 2082504433, 218262071, 2666551070, 3844955859, 1885787522, 50919684, 30300958, 3237830009, 1004399278, 1420324202, 2995067867, 3343455201, 1341482320, 2707911315, 2322962795, 104691279, 433113543, 1673935915, 237192280, 3866873407, 3719846074, 504926120, 1585743054, 710382710, 2276436306, 2976938826, 1322735386, 1856969923, 311925360, 1497000075, 2852252785, 207694370, 3237126868, 126779936, 696212993, 3860732454, 2811018481, 3182218492, 2694262689, 954054185, 1145279765, 1827792779, 647535690, 2378645894, 1603060963, 1501639457, 967601596, 3979534574, 2129057469, 1503074666, 3455573355, 1277747107, 2364423785, 718418781, 2029920441, 3230465514, 3292224990, 796319542, 4143628522, 2357283776, 3321794845, 2371483975, 1136784117, 2757314460, 132067372, 294498845, 2989608361, 1147501898, 848670725, 3702484846, 3398317762, 274118355, 3486956662, 2414417547, 4165976855, 3707418163, 3614978249, 793009306, 4227283826, 2072607460, 2291123052, 1319566667, 3736885972, 1075733989, 2822123350, 883768237, 165340447, 2283477403, 3854687889, 2702364501, 261781101, 4253180939, 1904200988, 3670999235, 2081253795, 1013385256, 3393606543, 3915738401, 3677841368, 2222722431, 3582521284, 2184635962, 1379820344, 4132361812, 3076369748, 3111110095, 1060089765, 3951504597, 276119608, 4292130693, 1208342406, 2964718231, 1156835032, 1503506724, 17689181, 1253790050, 2052448727, 3951262449, 1045066741, 1212371757, 3864687390, 2781636814, 4164334487, 1434750495, 1015217609, 492107542, 4106176432, 4258301116, 52857279, 3601017578, 553436516, 1286022350, 2970181802, 1531473162, 615711544, 2770114226, 3807138554, 1254115612, 405024141, 2248962327, 3661682788, 3457720992, 2391719239, 3782958744, 3184983441, 1120404266, 1505151243, 2382314268, 4164517871, 782247452, 923774834, 3508260701, 2537984828, 2116287910, 3255992169, 2640296699, 614769200, 767427138, 3456406779, 1809700841, 2437468993, 642938299, 3155191374, 4074085350, 2642920857, 3189984175, 3169851773, 4086000673, 2490375684, 3948311217, 3105674217, 1698869289, 1311043867, 193634359, 3011562913, 4136987101, 3694637471, 3746665664, 984905715, 1842085529, 2014624560, 1012559384, 381626366, 3316965712, 3951018504, 1396133012, 2477956684, 3892489603, 2447107565, 1585934707, 2614794953, 4048636321, 697301886, 2382428822, 2964257243, 506994596, 1901393962, 3958702238, 930275666, 3970480891, 2137671677, 911161575, 3800494155, 278586712, 1193762952, 154795879, 3301269187, 1668521332, 444082092, 1753908500, 1687735396, 3236812133, 2861130228, 179908202, 1539423798, 1280312575, 1354412234, 890265444, 3698680851, 653081540, 3681719879, 838283359, 969405299, 1918696509, 651424255, 1081467498, 1369194422, 969636592, 1353343686, 1151142771, 622249210, 2324152022, 3419137792, 2402401643, 417315756, 2283635979, 2730135008, 945357607, 1421847419, 546033882, 3198842674, 3343416782, 1103542692, 4192435052, 2680753787, 1928123125, 1829821471, 3877076359, 2319958157, 1817991563, 3019027601, 3350099005, 122241996, 2220681659, 1867304134, 3903645175, 3926484316, 561272258, 2924762331, 1521681554, 4276247138, 4264605013, 3489960755, 90524145, 3924010437, 2159859802, 3931840385, 1622645822, 3614003481, 4142324969, 2557247602, 4114169094, 2832266442, 1338437964, 4072229872, 3375287658, 2231757313, 4020609455, 2396693058, 2794056809, 1622056246, 3798643807, 3419424563, 1469037362, 3368075234, 2696057690, 4239384736, 2499585821, 488059987, 2262538463, 1978623658, 294535630, 3609960885, 432048986, 2518665415, 576966143, 1577963777, 3672258101, 1737846056, 1033455641, 3049863102, 414818580, 2310833967, 3876593023, 1159401619, 512103557, 3929750248, 104744865, 2294284829, 700010847, 3919829947, 472148418, 2495096228, 1476352517, 3466719922, 1423170701, 1835216137, 3804324362, 3156638174, 218238460, 2122719443, 1475392811, 4191547266, 1660363531, 1752963086, 814996542, 1775564261, 2768667643, 1691944624, 2673873848, 3717015687, 4274924722, 4267842589, 3218843587, 4086630122, 2525920765, 2642512022, 2581476770, 1587395043, 2479647167, 2075617909, 2220378822, 1164751823, 1254817289, 3012514369, 535781325, 1155411560, 3470618493, 3736078399, 727696447, 3668735551, 2540239292, 1287246718, 1034530277, 3398095154, 2277784043, 1007465081, 2592218771, 2307100491, 2280001478, 3781351274, 517873620, 16783814, 376212454, 1269327062, 2190745862]
    @u32_2.setter
    def u32_2(self,value):
        ca(value,[237099665, 1725693514, 3671290215, 2838122575, 2174235839, 1926762547, 837710207, 2675306390, 3296759548, 3236712776, 1185582523, 3424554628, 2120088772, 3672727628, 1229489468, 299615394, 2391828662, 2161918065, 3215046430, 4090719326, 4046969338, 2837195073, 1814520605, 3281278603, 2366669618, 889646058, 2889818005, 582950935, 1660657214, 3304485267, 3017091402, 4182786222, 381383578, 468232037, 4264726246, 548129943, 228487325, 1626908942, 3843628003, 340032714, 896193553, 1589965383, 421647904, 1025804481, 37483739, 314532432, 2655347560, 117434633, 503953090, 3976906518, 1323855325, 538108471, 4161859424, 1912643799, 1352908924, 3415941572, 2123957567, 2125372546, 3660361032, 2093953170, 844556942, 350952258, 3712309630, 1671728833, 1515702177, 674196370, 1804290265, 2369213421, 659681625, 3007121556, 3629421992, 2355746396, 1887771, 1763854265, 3669589284, 3060951582, 2289752966, 2753656458, 453476287, 3858397040, 1755557022, 1056528532, 1074824037, 3392115327, 959387159, 4047339053, 4055444899, 2701521116, 3269246259, 1658313101, 1191016218, 2976266754, 4058115909, 3148745595, 2255966436, 1286833652, 3846605743, 332980236, 2987111809, 2863137443, 3589002629, 3634508729, 3050304267, 426166523, 38644952, 4120741158, 3779249472, 2247004208, 3887627978, 771737466, 327488668, 2413511241, 3742352323, 1800531129, 3093397506, 119855689, 1044449337, 1621589532, 2435672368, 2249934961, 2486385468, 2733265378, 2055466545, 3463839050, 1741434858, 1937180913, 53147295, 380685724, 2147133772, 3377145922, 1696161493, 986108230, 552797714, 1030805428, 3633258771, 724378483, 1453096552, 3633745301, 722493301, 3218821892, 3672842476, 3232339885, 2194639207, 3626117658, 160139022, 1220950174, 1499215195, 2900860877, 1105932921, 2513047638, 2975567394, 2688547895, 1701949245, 494851022, 3099438803, 2302405511, 3002890773, 3694596195, 1818301109, 2241585621, 3375937719, 2173718080, 3174769392, 2332849203, 1120354034, 3688107993, 3910547603, 475511452, 165704715, 2543590060, 4279301981, 308235882, 1816022030, 2611287885, 2638354900, 1603444131, 2625463614, 2748122332, 2695819720, 3508062749, 4213882116, 1456900955, 2527945808, 1021825166, 2050461441, 2014465404, 1165369542, 1735932899, 3460204932, 1482933068, 1853558960, 3796877889, 2819245867, 1495722807, 286085468, 1232127264, 1369041740, 1203310608, 4013214417, 3662137316, 3906425458, 1886277730, 3592347464, 4124894145, 1520615672, 2057935984, 2780423261, 3807868959, 1096708615, 1133308613, 2081283278, 3031731081, 777297905, 728628197, 1045968931, 2798986608, 1441163940, 425803298, 3425923673, 3174138272, 225290447, 2789342514, 1500710940, 2214009944, 2611052505, 1511169866, 3468976229, 887023337, 3301621653, 348051316, 3413528372, 688050819, 3270149113, 2721404891, 2790531383, 1307526009, 24196953, 3323021735, 1883300819, 827261292, 1024782357, 4200877565, 961985674, 166365221, 3011947146, 3773678739, 3122249899, 4236359826, 3567170538, 164427914, 3384429677, 3901604544, 3178054797, 1736839253, 2964545385, 891428101, 1944593339, 1989423560, 1361523913, 3168022842, 3512787479, 1890231449, 1593427930, 4149710413, 206469070, 1896704648, 1231454209, 4068940405, 3271655038, 2008435184, 2914967896, 2357818161, 1859278865, 3410094777, 1298228364, 222292372, 1055108733, 4040689906, 2210549194, 1948747, 2506100330, 962472296, 1968083925, 113875684, 1936131419, 1016307414, 1060859451, 1739828182, 3346648079, 1164081840, 2485888280, 3476085289, 585721471, 390929102, 517669802, 2653223889, 1174053498, 1569525180, 3310507972, 1002962122, 2262804195, 3220775546, 3182459697, 2156503148, 4131684371, 2813459977, 1117022498, 1997829290, 2683851565, 107074302, 1419327824, 3915955155, 3780878619, 610899511, 1901058671, 4050293718, 2053491262, 1391571066, 1177627511, 743398950, 3803305715, 194123827, 3621325995, 472267748, 3375152783, 2897163902, 3462255512, 4250233830, 3994919468, 2831376517, 246739001, 2563541164, 2158887230, 3637942716, 2966210109, 47815115, 521677298, 645694605, 3228944885, 737962495, 826169136, 3548976344, 4043510480, 495863083, 777697689, 805624668, 1263172222, 3510345575, 1056092728, 2969537722, 747239264, 3369168528, 1344872701, 3335255317, 4214479629, 3890217901, 212326383, 626667851, 4084223303, 2815290146, 3385778156, 1708926854, 295550151, 494270470, 3067952778, 1533064310, 2934900292, 1705387163, 1307922285, 2193031516, 2433387564, 439649015, 2639844157, 3899988054, 3512645808, 4082111285, 39460185, 2109679546, 2807623639, 872015072, 980218181, 3396910791, 3668142418, 1001890199, 3235923562, 3566499716, 363410876, 2673237222, 573356352, 1636136151, 2224553312, 3704628010, 1623877736, 2563570732, 1232767726, 2971775467, 4216718036, 3488020769, 257411122, 1168087703, 818565641, 900860168, 1947568647, 164818961, 3931611634, 3720231207, 2690894061, 1424779930, 90538671, 131364160, 616530415, 743044912, 129491467, 4041759658, 3433286148, 4169430938, 2922959631, 3821215730, 3097046213, 3611435200, 2326824436, 184884915, 2069988071, 3914342196, 106319212, 1325869172, 3906567559, 1758481342, 1277175140, 2754342337, 1294820705, 791996734, 41241012, 3345622322, 3718866993, 1255338839, 1391956142, 3839078475, 3457508262, 551513656, 1004850662, 3795985935, 298265118, 3742037297, 3355517467, 3601723593, 3585988041, 3063759488, 3171470181, 4259702765, 3239000394, 2708065681, 4092601030, 346908933, 849213263, 2851377667, 1796454246, 2735073999, 2777745491, 2294240001, 2121652435, 2706284022, 585848169, 1936702478, 2371114722, 1541583037, 116304242, 3676364969, 3879455349, 3833621771, 3701696564, 2780518089, 1479844512, 1789233460, 2165430981, 3709637684, 1215700310, 3383152932, 2134182167, 3267525810, 4142614062, 1913035686, 299460925, 2677124325, 2261142050, 2007429043, 515722793, 25703755, 3410497288, 1661381183, 1667524384, 530887788, 3517835794, 159256235, 3805603779, 2368397, 2999883232, 39771046, 49747199, 3734347231, 185140859, 2259304947, 3389847559, 3758478898, 1438981583, 1923428196, 4294696986, 1917080172, 3599354053, 813437110])

    @property
    def i64_1(self):
        return -1357833931563696072
    @i64_1.setter
    def i64_1(self,value):
        if (value!=8621740821050813024): raise Exception()

    @property
    def i64_2(self):
        return [8621740821050813024, -9092072209079113602, -3056007272962959794, 5895514005284775249, 4825857599917744482, 2093519537988072834, -4390907564722863586, 8598973384036716702, -1889020672280261540, -8273635663381002611, -1941314642980235766, 1812319066748738475, 4190176042918780749, -4555199367311683530, 5467393609117797644, 8359783806563259266, 3800668915803924955, -2655932873935461949, 3136675805239089308, -3633713411557631382, -672757299114219972, 3045962201700775993, -3026485644327632861, -3372272670687649520, 3387661134442604201, 3677140703283269642, 4482422720713908644, 1337692977628619063, 6948420747960198793, -2492903114419653680, -5938903035079054289, -7806446185001452553, 9040686595201532492, -2127381394247868345, 8655785215940696615, 6435851473422996010, -8509497626685383427, 1304836616586909040, -2675436555158709746, 7454381249933066408, 1631169664587044350, 6013206163109033855, -2269271257167747155, 362749191994199052, -2710425314932035541, -3130715904393787670, -4410494504975660198, 4957729582609338569, -8246870151259110017, 6845983371242614475, -2258617392930568184, -8252230642158077029, 2670510062513563636, -6653455225739816423, 3093107250382849352, 1150551445512420048, 1546949923942708166, 5021898317351658427, 3707867854662121111, -1206055501856481918, -1873593186785558123, 6775838224715797812, -1115046710372778769, 528633723916988990, -4174382295242439358, -5547557100483108777, 5731859982382023557, 2204054933203810496, 3007479017130878933, 6608694896063582073, 1503694568421070630, 1248413523206321552, -6401043893159800201, 1353202742204949340, 2304302719445899395, -1291964394378923514, -5522844881206564639, -1277367478728568636, 1849991021787670735, 478721890957105862, 7757247149420834244, -373709650675810738, -5057614129950301004, 6162983513491054102, 3145006736835504836, 5885317631158909353, -7602326138257639761, -4157450027384868646, -1360567824864190920, 229176854089967110, -2202711857284656499, -2946750387084440631, -7399092435233174868, -931278862032913506, 8725183201793225879, 4422438402418122694, 7390489870132742668, 5253764508555093227, 1198113859723757987, 7260998365611273804, 1540767319493735478, -5799740479458549922, 1136167730386243597, 1413668892541509388, -8362134679601352333, 3664237052291625965, -7059531260401496534, 244969021945500288, 7960640458120876383, -2144041369569582147, -8542531942333624037, -6912033525905196529, 7309130333167087960, -1428796488709117140, 7889412153530907816, -6519274351560620428, -7194011194445795971, -2253470711475766161, 2052913415378741465, 8349030699411536987, 2962275883196204755, -8896757719886490153, -3481651114681941922, 9178906373760388169, -2393681984948405823, -4722899724188292419, 2219571189613806132, -8736536710280581263, -6631663654879231430, 1213083601717174358, 351791283162447724, -2728467560827636562, 2174378918144416458, 748751282949822397, 4251372914295826830, -4967177568325109568, 3825916028954041329, 7303839053387841791, 8648996684183789510, -6188350610717327471, -9016026939100696370, 8366545235017906362, -4151061240351591634, -3308165752571595210, 5710967263762362072, -7116887066458274066, 6003026705335466483, -2788076296930402698, -696935785960712847, -3523035848103775545, -4808396779515182120, -4487243801299967856, -316555344628268867, 2148745648896444003, -7908465185551702581, 209478862744791304, 8329349262325078360, 2312897865550480622, 3534430375708664567, -4313813383770928446, 7798388933635693783, 423303070618897314, -6223899204612392666, -7997497118304435999, 1761514773996835425, -8886871075540730292]
    @i64_2.setter
    def i64_2(self,value):
        ca(value,[-1418708830105823852, -1357833931563696072, -8308127073437794904, 6203263204523798112, 7076661289157584762, -3645491092747259726, 2969229117250121621, -8403401867791621438, -5706351777107258259, 6979420050019736435, 1350986631885231652, -8626678967587677100, 8380704325304801386, 3423582193572197909, 8713973059069583959, -4562940403005824119, 9144900318464157853, -8717799056344934090, -8792498500921807539, -8345039878076898189, 5201358909840838683, -3398583150340629128, -5482869438456886726, 1644815108571813337, 7248497692538999361, -1178045319005427907, -7220532561583062381, -2882504460577706964, -3460274637164886125, 9053064536664375063, -8649931456492292885, 72282480921257410, 3058905063630457969, 8394362105178121659, 8263211448476405605, 8671703720724529690, 1117912130945798022, -7392161278301566795, 9070973456367872189, 5064083874137910433, -2216141782782730608, 6092600172408194906, -7328184273434559673, 7340896108422144895, 8041029351530593362, 3567042073657363684, 6634152186323571334, -939114094925119978, 3932918768588612631, 2223869457290740495, -1394521432769550065, -7708491921728269104, 2558409591077932690, 7323090212396920736, 4463226188281322565, -7684442752899854301, 3813932804031799733, -3061288894555894392, -8926314527654650550, -5483212417699975352, -5168152193234004511, -5252714907036148733, -8899682260331039592, -6945672564712903320, 1843836835216653982, 6265565553002088665, -9191803385169282118, 824381268893232707, -4195712559860724390, 3170122388521742267, 93238405484244323, -3808714570016938587, 7751370385159261162, -415651213975075366, -400640794129234242, -3632420176870277542, 2145224332581955327, 8408764257602201311, -5753925773175608181, 2442171188911603754, -718254550700219999, -5279112326876598860, 7731819115318618935, 7285784364016347384, 6648758251111712748, -4965048064766122366, 1799714525316551079, 5808264002475810898, -521447549589589148, 263148779791826658, -1256378489223837059, 3001523551318331984, -2133704098322946340, 9175731965505830169, -275510851941027307, -3450575930678805596, -4673869135690784872, -2779584507299050825, -6244919930307138446, 5663020090027727817, 3592337319079719462, -7699870730217589682, 3427192886285003578, -566635025493084181, 2780130284244381358, 3422425913941932991, -723427948584706426, -1731222455107826641, -3556462521989327042, -8514332474959779238, 3681987062303886320, 1266418540216073989, 4892980044242035752, -5243563662285950589, -8021867029688739836, -5712778566201121978, -2133887347488624783, -667985954315002704, 2350239843243973147, 5123432618264623922, -271741713269398666, 8726020244487579882, 3802883727236102212, 4050625489658817027, 6873081973971784099, -7507676454188557650, -675853520577120389, 4704868291861385417, 1767091830085798988, 1315143445596137295, -8400502078442130692, 4250620495159315861, 7743903342313618441, 8236285998949285411, 920705431865098656, -2187810178560173353, -5636947816335562469, -8869870121412151030])

    @property
    def u64_1(self):
        return 13389861970863644378
    @u64_1.setter
    def u64_1(self,value):
        if (value!=1465640522145789825): raise Exception()

    @property
    def u64_2(self):
        return [17812699909525330179, 13389861970863644378, 16257896157253761478, 14191477546208115816, 1387441194387183523, 8800889055657239662, 3787113061722336589, 2075067786453142295, 2302772129471114307, 16660993589300385169, 5227667125318999851, 17211198982499914739, 13967365476154884537, 6210802835678950626, 413837793611927178, 15016088479821729126, 14194309003275915218, 5521545037113246785, 9721585675207248367, 2487154057124779480, 4054392452442988950, 15742440468026600431, 8404041348136789525, 5704587169648799325, 8615894037736189999, 7555294940121326684, 166204857340424907, 10630415758080788319, 3699593146963368456, 15841753586674104403, 1425904355269403798, 6757749835782369274, 6484708862168533651, 14311810156028177789, 13305336491678304892, 9547219694933920657, 16939089102075290494, 13780222831094724753, 729578726262763066, 6741605646549400625, 860499368566843233, 4821657628681234936, 10629375059978179469, 12676697982045410789, 7965873501849669898, 6463814633396676710, 10304605129170106831, 17634109250944839532, 7874201956261190767, 2093432098376142516, 15162293521637815459, 14480915389905814968, 12246183009228206627, 9927056522845945393, 10708714764412026102, 12620101894595011829, 9720992984909508434, 1335165052342958298, 3842118717279685369, 5703296853718993513, 10169884007081888934, 2514628960699067131, 5254570865582417565, 9562135776312844762, 27891557900731192, 14886705471885923481, 3399688988254798568, 14640082747632735324, 12221809011211673821, 12865683977160344326, 12797396568995658538, 16277433856161229511, 5834216036130347946, 41836075316600799, 6171722505441450511, 8601242920007887523, 13624814788188880079, 7848598808818978240, 14273686016064474182, 9616131192223535887, 17907341921682029586, 10138262866472100954, 14661185914352643699, 18102813560908894003, 12307841218657619289, 14709882437025014177, 10238864911411793767, 4776457610936466600, 8782354639535937976, 18274481696525890320, 13992637006136445380, 11566349649437476293, 1209664843394078754, 14394522101288007152, 2915009092315033094, 182528511086129450, 15695741318843217573, 744918667092745933, 7146826536782008676, 13838640680680387773, 6708462726963541522, 7741352156378706754, 15062394166759350529, 10613549923461193838, 11002287295489384645, 11112868002985992483, 14972199425906445655, 15176061787056984512, 3369667758791907709, 10545737311162535909, 10549452773932875360, 977025607559254534, 8213649184128301518, 16026014660753415782, 16346803042848708719, 8641570190583236526, 10372374375551503871, 8475065376071450531, 9492316019190861724, 7258336917778003543, 7704933404615957344, 14492234026024540236]
    @u64_2.setter
    def u64_2(self,value):
        ca(value,[6515978873578326855, 1465640522145789825, 14139647178981527348, 17376225719361197745, 4827355217349405315, 5237172857588412536, 11185863429255124449, 11922950710462888186, 9723873762901963012, 2360891509504070464, 17595800616336901155, 4676383109049523121, 5519403084078587651, 15199794964642249670, 10725748072798711186, 11861452006494413908, 10866242934922922899, 15599520359228044898, 4022505103249338009, 15081262745932646374, 9978655822822015426, 1893338345735521355, 8335612627840221039, 13125076221780371251, 1843608744939432450, 1877855184169582147, 360237399108374165, 14133486497511175136, 6918428392028668980, 4207262405010786686, 11882372330517522341, 2660307236802524516, 16105897257753062921, 2353931053072926625, 10173424970756197713, 3742480367255311168, 1303431584704287527, 12527899890265500372, 32220987555692133, 17556513786877588779, 14599571048880016586, 2017220613051019209, 13580232873699969747, 3864855431338072766, 10522968089599101769, 445176367690966897, 7790111520686478868, 6394442284921113988, 16995884223523288612, 11216569412804039035, 4321418227933556664, 5409834497962741327, 690550291029646943, 16074599988808644612, 11236550486638087434, 6844569081007881849, 5869987636307743707, 7778211196101597376, 15853871901637280370, 18058575643888946512, 14027203060397441285, 12712062502708340258, 4041613882264720796, 11645048579559315688, 1246226537584125354, 3474795601576826029, 11513896830487717539, 1974322205737539934, 17242471345616954213, 8678121572397745114, 17527671945381764646, 5033231148296076497, 6411880965725185093, 174473638020748044, 8158678930583416018, 9507609436552652251, 16205993571484058929, 8035338227846555833, 8791374446603527925, 14595445946451526244, 5169961786923105799, 13397974474224235898, 2364042737119390982, 5321299597050057517, 1121024914655468441, 12207167839097364776, 12619831538472755181, 4864354177058320218, 17848460798228747459, 13261044407690283599, 10209900008497671979, 6862409070349488681, 1432310611369939292, 2092522766869471913, 15058223303172327711, 4178174561433201628, 12906394038648389198, 15191542062580018441, 16452252929507747318, 11201120125455394600, 6726163449083399053, 8426476024479275017, 7026246701397961488, 9033438331677737541, 5951673483825817230, 10638919135849238472, 3252342350133602871, 15766880131631627052, 12385842632184481382, 2748643971592610065, 6396730451340699978, 13659499533346384982, 4282043305472384300, 1711405441567413160, 17992713571449412921, 3556627233283536994, 4138074248161109398, 1622144212241737621, 18087263875532968938, 14104137172003718411, 7644309790031389842, 8816844725250613052, 11421439960737023984, 10454322951672789795, 2119200398037807197, 8384409476347314289, 2527068029837223073, 4862875043870995989, 17581079332542377528, 18385625565005546141, 5262116103886681622, 14174635193688816521, 3985859099523137999, 5526499814203466410, 1239704066545123753, 5917443538249299253, 878138865084935513, 10218107935864045533, 6547939038367120283, 7353731416371741667, 5504609912290331194, 17697030959073472945, 3134771705926671223, 1308908721146697947, 10579235124105673010, 17332984836700322102, 13722665407351335633, 18423215754649979094, 3171161736406578023, 4234709098044006158, 7347564326123203638, 8195365762234651673, 7781698260938130820, 1180819293191049424, 493531138123366511, 1365828412106184272, 10313217779396245974, 7602972172978537794, 6065626025778962290, 9672897350080504270])

    @property
    def str1(self):
        return "Hello Client!"
    @str1.setter
    def str1(self,value):
        if (value!="Hello Server!"): raise Exception()

    @property
    def struct1(self):
        s1=RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct1")
        s1.dat1=[2.416507e+16, 4.573981e-21, 3.468194e+10, -2.393703e-06, 4.937973e-15, 4.706768e+14, 4.286830e-10, -1.090462e-14, 2.238670e+03, -1.254407e+14, -1.275776e-21, -4.124599e-10, -4.953108e+11, 2.808033e+03, 4.685151e+14, 3.710607e-08, 3.523588e-01, -5.585682e-20, -3.290719e+08, 1.600972e+17, 4.257210e+16, 1.114490e+04, 2.739939e-10, -4.332717e+16, 3.482223e+00, -2.162451e+10, -4.527774e-04, 8.558987e-19, 3.755463e-12, 3.863392e-08, -8.351348e-05, 4.774283e+02, -4.612524e-06, 2.206343e-06, -2.767520e-17, -4.183387e+08, -2.037466e-19, -1.780912e-18, 1.656909e-07, 4.799751e+07, -3.604348e-06, -3.146762e+08, -3.709450e+15, -2.379431e-09, -3.034066e+05, -3.072796e+01, -1.057111e-14, 4.753235e+07, -2.725014e+07, -4.895406e-20, 5.339502e-20, 9.375211e-11, 1.632454e-03, 1.051386e+01, 1.915580e+17, -1.999453e-09, -3.087190e-02, -3.222377e+15, 4.219576e+03, -1.401039e+05, 3.950473e-15, -1.620577e+10]
        s1.str2="Hello world!"
        s1.vec3={1 : "Hello Client!", 2 : "Hello Client, again", 4372 : "This is yet another test string"}
        s1.dict4={"teststring1" : "Hello Client!", "teststring2" : "Hello Client, again", "anotherstr" : "This is yet another test string"}
        s1.struct1=RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2")
        s1.struct1.mydat=[-2.457273e-05, -3.349504e-13, 4.139542e-09, -3.944556e+04, 2.761296e+04, 8.570027e+16, -2.472613e-03, -2.096009e+03, -4.186716e+10, 4.584716e-20, 3.951344e-03, 4.557915e+05, -7.117988e+03, -4.605957e+11, 7.353630e-10, -3.303575e-19, 6.133982e+05, 4.528668e+01, -1.427778e-11, -3.509465e+15, 1.695706e-04, 1.732872e+14, -6.370107e+01, 3.269065e-06, 4.480613e+03, 2.058970e-06, -3.748223e+05, -1.507989e-09, 1.690251e+19, -2.177567e-08, -2.391641e+16, 3.617128e+03, 2.568296e+15, -3.009031e-07, -3.754976e-09, 2.458890e-06, -3.800108e-11, 1.555663e-11, -2.085887e+18, 8.574830e-22, -7.228491e-13, -3.987643e-10, -4.777544e-02, 3.908200e+04, 4.221779e+11, -7.528852e+06, -2.077042e-19, 4.478813e-02, 3.506975e-06, 1.011231e+12, -2.181961e+17, -5.098346e+16, -3.791130e+06, -2.734203e-14, 6.340994e-13, -4.582535e+07, 3.977645e-06, -3.785260e-07, -4.102542e+06, 4.751411e-16, 4.203566e-14, -3.894958e+00, -4.585783e-14, 2.432993e+15, -3.592680e+14, -1.560186e-12]
        s1_dstruct2_1=RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2")
        s1_dstruct2_1.mydat=[3.785355e-17, -2.518001e+17, 4.016500e+08, 6.566648e-04, 1.284318e+07, -2.674821e-13, -4.955749e-14, -1.699098e+00, 2.901400e+05, 1.499143e+13, -2.252822e-05, -2.653172e-14, -2.482811e+07, 2.353638e+18, -2.177258e+17, -4.715112e+06, 4.508858e-18, 1.205611e+17, -3.469181e+00, 2.383792e-13, 4.544766e+14, -3.029250e-05, -2.545049e+05, 3.149303e+19, -3.724982e-10, 4.066723e-02, 2.809941e-08, 1.279689e-20, -3.303471e-09, 1.846558e+08, 1.311495e-06, -1.185646e+04, -2.603100e-19, -3.519314e-17, -1.595996e+04, 9.735534e-20, 1.234003e-04, -9.697458e+08, -4.895883e-02, 4.770089e-16, 3.757918e-11, 5.253446e+18, 5.071614e-13, 3.793300e-08, -1.993536e+12, -1.846007e-11, -3.458666e+03, -3.995887e-10]
        s1_dstruct2_2=RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2")
        s1_dstruct2_2.mydat=[4.856615e+15, 5.981566e-22, 1.433616e+14, 1.747102e-09, 2.850376e+06, -3.748685e-08, -4.969544e-21, 2.530419e-01, 4.393913e-09, 3.837331e+04, -4.315065e-04, -1.073834e-17, 1.244057e-15, 3.901853e-10, -2.725237e+10, 2.896243e-18, 3.609897e-13, -1.937982e+02]
        s1.dstruct2={"test1" : s1_dstruct2_1, "anothertest" : s1_dstruct2_2}
        s1.multidimarray=MultiDimArray([10, 10],[3.489074e-03, 4.416440e+12, 1.069372e+12, -3.678917e+01, 3.617865e+03, 2.631290e+07, -1.012036e+06, -4.990820e+01, -4.607768e+10, -1.205544e+18, 3.384829e-05, -2.739955e+12, 4.098031e-13, 2.170650e+15, 3.313171e-07, -1.107813e-03, -4.840364e+09, 3.470747e-08, -2.945301e-13, 4.900611e+00, 2.494936e-11, -3.705569e-06, 1.189413e-03, 3.034111e+08, -4.905472e-17, -3.857051e-07, -2.096687e-19, -1.795052e-06, 2.523800e-18, 7.860593e-02, 3.519022e-16, 1.236777e+12, 2.636618e-10, 4.386448e-06, -2.513132e+03, 1.400490e+18, -3.156777e+15, 1.661838e-07, 1.652002e-01, 3.732142e-17, -2.562672e+10, -1.965676e+08, -5.664540e-01, -3.224055e-17, -2.842033e+18, 4.816053e+11, 2.517680e-08, -6.443991e+02, -4.267612e-21, -3.524623e+02, 3.760018e-10, 1.060012e-06, -4.158190e-01, -1.969302e+14, -3.838685e+16, 4.574934e-09, -2.832637e-09, 1.005947e+06, 2.388806e-15, 2.331301e+15, -4.602999e-13, 1.987431e-20, -2.190281e-03, 3.648919e-08, 7.198137e+07, 1.772828e+02, 3.444774e-20, 6.255538e+07, -2.058346e-02, 6.081334e-02, 4.300420e+12, -7.901606e+03, 9.496649e-13, -2.206441e+09, -4.628939e+00, 1.660493e+01, -3.623921e-09])
        s1.var3=RobotRaconteurVarValue("This is a vartype string","string")
        return s1

    @struct1.setter
    def struct1(self,value):
        ca(value.dat1,[1.139065e-13, -1.909737e+06, 2.922498e+18, -1.566896e+15, 3.962168e+17, -3.165123e+17, -1.136212e+13, 3.041245e+16, -4.181809e-18, 3.605211e-18, -3.326815e-15, -4.686443e+05, -1.412792e+02, -3.823811e-14, -6.378268e-09, 1.260742e-14, -2.136740e-16, -4.074535e-10, 2.218924e+01, -3.400058e-08, 2.272064e+02, -2.982901e-21, 4.939616e-19, -4.745500e+03, -1.985464e+16, 3.374194e-04, -8.740159e-09, 1.470782e-06, -2.053287e+06, 4.007725e-13, -1.598806e-13, 2.693773e-06, -3.538743e-08, 4.854976e-16, -4.778583e-12, 3.069631e+06, -3.749499e+03, 3.995802e+05, -2.864014e+13, 1.276877e-13, -4.479297e-02, -9.546403e-13, 8.708525e+06, 3.800176e+04, 4.147260e+10, 2.252187e-20, 9.565646e-14, 4.177809e+13, 3.032250e+01, 3.508303e+10, -4.579380e-17, 1.128779e+05, -1.064335e+11, 1.795376e-06, -1.903884e+09, 2.699039e-03, 3.658452e+15, 4.534803e+15, 1.366079e-03, -3.557323e+07, -4.920382e+18, -3.358988e-07, -4.024967e-11, -4.784915e+16, 1.490340e-18, -4.343678e+08, -1.955643e+14])
        if (value.str2!="Hello world 2!"): raise Exception()
        if (len(value.vec3)!=4): raise Exception()
        if (value.vec3[10]!="Hello Server!"): raise Exception()
        if (value.vec3[11]!="Hello Server, again"): raise Exception()
        if (value.vec3[46372]!="Test string!"): raise Exception()
        if (value.vec3[46373]!="Test string again"): raise Exception()
        if (len(value.dict4)!=2): raise Exception()
        if (value.dict4["cteststring1"]!="Hello Server!"): raise Exception()
        if (value.dict4["cteststring2"]!="Hello Server, again"): raise Exception()
        ca(value.struct1.mydat,[1.783093e+12, -2.874045e-19, -2.311319e-19, -3.099234e-12, 1.000951e+16, 3.775247e-12, -5.853550e-18, 3.175537e-10, -3.112089e+08, -1.577799e-06, -1.379590e+00, 4.777044e+13, 4.811910e+18, 4.736088e-11, 1.770572e-08, 2.713978e-22, -1.649841e-12, -2.486590e+10, 4.092716e-18, 8.724120e-03, -1.183435e+18, -3.904438e+08, -1.251365e-11, -4.007750e+19, -2.206836e-16, 4.014728e-13, -3.960975e-12, 7.192824e+05, 1.981836e+04, 1.840814e+16, 1.488579e-16, -4.862226e-06, 1.612923e-17, -4.978203e-04, -2.305889e-02, 7.627221e+13, 4.014563e-03, 2.388221e-03, -1.129986e-02, 4.055276e+10, 3.842121e-10, -8.588514e-04, 1.299077e-12, -3.331850e-12, 4.863277e-01, -2.250328e-11, -2.261245e+04, -2.770899e+09, -4.710672e-15, -2.267765e+06, 1.582168e-09, 3.664505e-06, -1.507921e+12, 5.460120e+09, -3.256706e-15, 3.012178e-12, 2.274894e+15, -9.664342e-18, -2.770443e-15, -1.955281e-06, 4.768349e+01, -7.679375e-19, 2.774544e-17, -4.928044e-17, 7.602063e-15, 2.506718e-12, -2.794058e+11, 4.329292e+03, -4.041289e-02, 4.035282e-19, 8.577361e-04, 4.197333e-18, -3.509270e-01, -1.711871e-12, 4.578825e-02, -8.783497e-13, 3.862885e+17, 4.219735e+13, 4.281035e-21, 3.323068e-03, 4.931847e-11, 4.032955e-21, -4.373013e-03, 1.592633e-16, -4.484112e-16])
        if (len(value.dstruct2)!=2): raise Exception()
        ca (value.dstruct2["ctest1"].mydat,[4.122753e+13, -2.656829e-13, 1.813864e-04, -4.675181e-05, 1.759511e-19, 3.517805e+10, -7.912215e+01, 7.708557e-07, 2.434017e-21, -2.540544e+00, -9.412568e+15, -2.124215e-18, 2.797799e+13, -2.240464e-07, 2.780110e-12, -1.025574e-14, -3.762272e-09, -5.715981e-02, 1.839704e-21, -4.719538e-15, 3.148156e-06, 3.483886e-12, 3.484006e-02, -4.544817e-08, 3.200642e+00, 4.503141e+07, -4.077123e+04, -2.776985e+00, -2.900651e-18, -1.463711e+08, -3.460292e-03, 2.348911e-18, -3.704219e+08, -3.275364e+05, 4.613595e-01, 4.867108e+16, 4.114866e-10, 3.070767e+17, 4.662623e+01])
        ca(value.dstruct2["anothertest"].mydat,[-1.037656e+15, -3.782364e-06, 4.982303e+06, -5.510401e-07, 4.271118e-02, -1.718093e+11, -2.644457e+01, -2.374043e-08, 1.729038e-14, 3.370840e+10, 4.302550e-13, 2.643402e+14, 3.199649e+01, 4.620204e-08, 1.323645e+00, -4.337167e-07, -5.003428e+11, 4.176127e+13, 3.324907e-09, -4.207938e-09, -3.324360e-15, 3.317889e+00, 1.775668e+07, -1.295276e-15, -1.610388e-05, 3.417067e-02, -4.874588e+04, -2.109628e+12, 3.130648e+09, 1.898554e-13, 2.421724e-01, 4.227281e-08, 4.844407e+19, -4.490481e+10, 2.599780e+00, 4.039296e+06, -2.944167e-03, -7.388370e+08, -4.473409e-02])
        ca(value.multidimarray.Dims,[10,10])
        ca(value.multidimarray.Real,[2.607856e-05, -4.060588e-01, 1.459089e-19, 7.661488e+12, -3.054205e+15, -3.953672e+18, 3.981083e-09, 2.023530e+10, 3.341041e-21, 3.927871e-04, -4.843469e+01, 2.836056e-20, -3.148469e-04, 2.672701e-06, 3.588983e+08, 2.702981e-17, 4.366455e-06, 1.595520e+11, 3.130938e+09, 4.453168e+10, 9.627982e-12, -3.824527e-11, 4.172935e-20, 6.284725e+03, -9.490302e-13, -2.151807e+18, 2.926671e-02, -1.089334e+02, 2.671842e+17, 2.174924e+06, -1.772301e-19, -1.809115e+08, 3.058543e-06, -1.098521e-18, -7.276741e+01, 6.617143e-22, 2.181270e-03, -4.632712e+08, 1.067154e-11, -1.149804e-12, -2.883778e+07, -2.772835e-15, -7.289469e-04, -2.053436e-01, -4.477369e-19, -4.906893e+10, -3.005378e-02, -7.615476e+07, -9.075230e-20, 3.684300e-04, 2.884596e-05, 3.589573e-06, 3.938783e+11, 2.541751e-08, -6.447446e+09, -8.709398e-02, -9.877435e-20, 1.430333e+14, 1.961905e-17, -4.892539e-05, 2.650625e-02, -4.408943e+01, 2.800706e-20, -1.087373e-03, -1.081200e-03, -3.748735e-10, -4.052447e+03, -1.102631e+02, 6.629702e-17, -1.349501e+10, -3.396688e+03, 1.492315e-01, -3.770557e+07, 4.248273e+11, -5.822309e-02, -2.695009e+18, -2.544586e+16, -2.923482e-20, 2.842902e-08, 2.007452e+00, 1.684762e-04, -4.948805e+14, -3.964645e-16, 4.261808e-05, -2.513086e+17, -1.863688e+01, 2.786936e+17, 2.306164e-12, -4.813284e-02, -3.734933e-15, 1.986399e-02, -2.682815e-14, 2.293712e-07, 1.247696e-01, -2.455383e+19, 2.697551e-09, 1.274751e+09, 2.041100e-15, 6.322583e-08, 3.443236e+00])
        ca(value.var3.data,[6.404176e-12, 9.258110e-03, 8.657620e-03, -2.064381e+00, 5.182360e-16, 4.167658e-16, -4.533051e-19, 5.357520e+18, -4.990383e-13, 2.286982e+08, -4.727256e-18, 1.465299e-17, 3.000340e-10, -2.304453e-04])

    @property
    def struct2(self):
        out=RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2")
        out.mydat=[-4.415088e+16, -2.033093e-17, 3.634431e-17, 2.030794e-03, 4.464343e-14, -4.137056e+11, 3.609991e-16, 4.332970e-11, 1.327470e-06, -3.304680e+02, 3.184654e-08, 1.194960e-16, -2.958549e+05, -3.320274e+13, 3.486845e-05, 2.878185e-10, -2.982726e-12, -3.653410e-06, 2.059068e+00, 1.150498e+16, -3.647068e+18, -3.847760e+03, -4.333684e-21, -2.357376e-07, -2.560470e-09, 2.931250e-15, 4.966713e-21, 2.960478e-14, -1.959583e+03, 4.593629e-16, 4.193491e-07, 5.941674e+14, 2.198075e+05, 1.487817e-20, -4.643292e+06, 2.543864e-14, 9.478332e+04, 2.948237e+13, -3.144190e-17, -1.369134e+11, -4.908672e-18, -3.581399e-21, -1.682968e-14, -8.984437e-02, 3.067043e-19, -3.361220e+14, -2.591105e-10, -2.119291e-13, 7.649594e+03, -1.869427e-01, -3.403057e+11, -4.798229e-09, -4.120069e+04, 3.384741e-12, 4.697254e-10, -3.594572e-02, -1.973059e+12, -2.627069e-21, 4.096077e-20, 1.629242e-20, -1.561816e+11, 3.240449e+07, -3.967391e+08, 4.635131e-14, -3.436364e-17, 1.485817e-15, -2.145973e+18, 1.160688e+19, 3.266439e+11, 1.686854e+02, -4.048943e+00, -2.905109e+17, -3.953827e+15, -2.855712e+10, -1.197294e-02, -1.997014e+14, 3.951602e+08, 1.287972e+18, -4.228933e+08, 4.212816e-06, -1.252397e+15, 3.517842e+12, -3.315039e-17, -1.816738e+19, 3.595783e+14, -2.834015e-08, 3.436611e+04, -4.192603e+12, 1.152454e+11, -9.405739e-21, -1.862898e+17, -3.811397e-10, 4.486272e+00, 3.666408e+14, -2.681908e-10, -4.859125e+08, -3.593152e+04, -1.883343e-03, -2.445939e-08, 4.540371e+01]
        return out
    @struct2.setter
    def struct2(self,value):
        ca(value.mydat,[-1.451096e-09, -3.762302e-18, 2.016877e+04, -4.171245e+16, 1.500851e+09, -3.071385e-05, 1.329949e+09, 9.439580e-14, 8.652806e-06, -2.729712e-17, -1.664008e-09, 3.787440e-16, -4.281157e-20, -8.703642e-07, 7.130173e-13, 1.162347e-04, -2.485922e-01, 8.924836e+13, 2.150995e+18, -1.816269e-08, 3.572064e-06, -1.020374e+19, -2.467612e-05, 1.294111e-21, 3.030328e-11, 1.736324e+04, 4.221306e+17, -2.544109e+09, 1.047630e-04, 2.082666e+04, -4.120572e-04, -4.550228e-11, -4.959645e+00, 3.988634e-06, -2.901463e-06, 4.379435e+14, 3.697324e+17, -3.285280e+00, -4.491892e-21, 4.962405e-03, -4.143004e-05, 4.447309e+01, 3.196998e-04, -1.679927e+06, -1.859794e+19, -2.749978e-17, -9.042867e+14, 3.970588e+06, -2.359863e-19, 4.923781e-03, 3.689224e-03, 1.741368e-14, -4.943555e-15, -2.473041e-09, -1.687125e-12, 4.622096e+17, 2.456838e-17, -4.076597e+07, -4.082942e-21, -4.483141e+19, 2.463502e-01, -1.818087e+04, 1.094518e+14, 7.514618e+03, -1.175704e-07, -3.071050e+18, -8.006996e-20, 1.363550e-14, -6.753529e+08, -4.661760e+15, -2.475629e-01, -1.282411e+16, -6.328699e-04, 4.898115e+00, 6.921801e-14, 9.951973e+01, 1.669967e-08, -3.750408e-19, -3.363050e-10, -2.470083e-09, 1.544354e-05, -2.844838e-09, 4.426875e+02, 3.468203e-17, -2.376018e+07, -1.431106e+08, -6.900572e-18, -4.640801e+07, 9.947893e+14, -1.166791e+10, -3.478840e+19, -3.103020e-09, -3.256701e+00, 4.374203e-14, 4.655054e-04, -4.106246e-17, 2.373568e+15, -1.319790e-04, 1.485607e+02, -4.933523e-05])

    @property
    def struct3(self):
        out=RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService2.ostruct2")
        out.a1=[-8.483090e-19, -4.401548e-08, 3.908118e+00, 2.063513e-18, 4.237047e+18, -1.124681e-16, 3.924541e-01, -2.184335e-10, -1.978950e+11, 1.586365e+18, 1.712393e+00, -6.314723e+00, 1.196777e-16, -2.748704e-08, -1.289967e+02, -4.051137e+17, -1.902860e+10, -2.070486e+08, 3.622651e+06, 1.315398e+17]
        return out
    @struct3.setter
    def struct3(self,value):
        ca(value.a1,[-2.426765e+05, -9.410735e+01, -1.667915e+12, -4.084240e-05, 3.199460e+03, 8.256717e-12, -4.772119e-11, -1.061407e-13, 2.759750e+02, -1.212549e+10, 7.012690e+15, 3.953354e+04, -2.617985e-07, 1.104408e-21, -3.889366e+00, 4.549493e+16, -1.376791e+15, -3.445205e-21, 2.137830e-14, 4.620179e+18])

    @property
    def is_d1(self):
        return {9285 : 1.643392e-01, 74822 : 1.537133e+09, 4 : 1.369505e-03}
    @is_d1.setter
    def is_d1(self,value):
        if (len(value)!=3): raise Exception()
        if (value[928]!=4.074501e-07): raise Exception()
        if (value[394820]!= -4.535303e+05): raise Exception()
        if (value[623]!=-2.956241e-20): raise Exception()

    @property
    def is_d2(self):
        return {"testval1" : -1.079664e+16, "testval2" : 2.224846e+00}
    @is_d2.setter
    def is_d2(self,value):
        if (len(value)!=2): raise Exception()
        if (value["testval3"]!=5.242474e+10): raise Exception()
        if (value["testval4"]!=2.208636e+08): raise Exception()

    @property
    def is_d3(self):
        out={}
        out[12]= [8.609080e-13, 3.946603e+03, 2.994203e-10, 3.200877e+14, 1.747361e-09, 2.827056e-16, -3.676613e-18, 1.886901e-14, -9.970511e-12, 1.932468e-18, -3.629253e-05, 4.903023e-12, -3.919949e-10, 4.982164e+07, 3.823096e-20, -4.044068e-13, 3.114078e+09, 7.572697e-12, -2.619929e+04, -3.882046e+01]
        out[832]= [4.750899e+00, 3.924377e+18, -2.735066e+17, 4.095362e-21, -2.407932e+09, 4.059499e+10, 1.376975e-10, -8.547220e-21, -1.344568e-20, 2.809398e+03, 2.118944e-06, 2.435328e-03, -1.410999e-12, 9.907226e-04, -9.745948e-20, 1.270118e+15, -2.833333e+05, 1.032636e-10, 5.312574e+13, -2.651512e+02]
        return out
    @is_d3.setter
    def is_d3(self,value):
        if (len(value)!=2): raise Exception()
        ca(value[47], [4.335907e-08, -3.270294e-03, 1.752801e-01, 1.235219e-20, -4.348647e+02, -4.503864e-21, -3.316231e+15, -2.080056e+17, 1.813854e+13, -3.380846e-05, 4.350998e+03, 4.539570e+11, 8.981827e+09, 3.326114e+01, 2.975688e+06, -1.017456e-12, 2.989498e-03, 2.842392e-03, -1.258677e-21, 1.068563e-15])
        ca(value[324], [3.239279e+12, 1.047689e+17, -1.236114e+17, -4.002822e-17, 2.657374e-03, 7.383907e-19, -5.067889e-13, -4.195122e-12, 3.642885e-01, -2.946040e+14, 5.522403e-08, 6.603132e+04, 1.464154e+05, -1.851534e-08, 2.808294e-13, -2.702278e-11, 3.850704e-06, -2.453957e+02, -3.015401e-02, 1.654070e+05])

    @property
    def is_d4(self):
        out={}
        out["testval1"]= [1.113851e-04, 3.830104e+07, 4.571169e-21, -4.064180e-05, 2.889736e+01, -1.790060e-06, 4.608538e+00, 4.687713e-04, 1.387717e-08, 3.914187e-18, -5.618118e-06, 1.530811e+05, -5.848922e-11, -3.397558e-20, -6.597368e-08, -3.779049e-06, 2.406033e-19, 2.507939e-10, 3.246113e-20, 1.341205e+16]
        out["testval2"]= [-3.088190e-13, -4.033334e-20, 4.150103e-21, -6.610855e+17, 3.688824e-13, -3.208025e+13, -5.034888e-11, -4.098363e-06, -1.272830e-03, 2.748392e-03, -2.644272e-06, -4.810065e-18, 4.629861e-19, -5.444015e-03, 4.046008e+17, -3.548079e+12, -3.455290e+16, -3.668946e-12, -3.522178e-01, -1.537583e+14]
        return out
    @is_d4.setter
    def is_d4(self,value):
        if (len(value)!=2): raise Exception()
        ca(value["testval3"], [1.771838e+06, 3.037284e-01, -1.739742e-02, 1.399508e-20, 3.605232e-21, 3.517522e+14, 4.887514e+14, 3.505442e-03, -3.968972e+18, 1.422037e-20, 2.596937e-21, 4.852833e-11, 6.852955e-17, 4.765526e-12, -3.445954e+16, 2.322531e-14, -1.755122e-12, 3.941875e+00, 8.877046e-13, 2.818923e-02])
        ca(value["testval4"], [4.146439e+16, 2.923439e-07, 3.549608e+16, -1.664891e-01, -4.192309e-15, 3.857317e+05, -1.101076e+00, 1.213105e+19, 3.237584e-14, -2.421219e-06, -4.603196e-05, -3.719535e-10, 1.124961e+06, 2.032849e+10, 4.639704e-22, 3.946835e+01, -9.267263e+01, -4.456188e+11, 3.470487e+08, 7.918764e+10])

    @property
    def is_d5(self):
        out={}
        out1=MultiDimArray([10, 10], [-2.240130e+14, 1.609980e+16, -1.794755e+07, 8.108785e+17, -2.296286e+08, -2.689029e+13, 2.036672e+07, -4.822871e-02, 4.070748e-05, -2.894952e-04, -1.728526e+17, 4.077694e-19, -2.977734e+13, -9.428667e+03, 2.672315e-08, -1.844359e+19, 4.243010e+09, 4.592716e-01, -3.792531e+10, 3.117892e+04, -1.830821e-16, -3.702984e-18, -1.957300e+12, 9.017553e+12, -2.184986e-17, 1.436890e-02, 4.008279e-12, -2.407568e+10, -3.170667e-07, -2.315539e+16, 6.646599e+09, 2.443847e-01, 1.928730e-21, 3.089540e+00, 2.813232e-02, 1.352336e-21, -3.562256e+05, 3.778036e+08, -3.726478e-13, 3.112159e+15, 3.573414e+17, 3.607559e+09, -2.923247e-19, -2.079346e+14, -4.611547e-16, 2.200040e+00, 3.670772e+07, -4.176987e-20, 2.086575e+06, -2.388241e+01, -3.759717e-19, -2.232760e-01, 9.066157e-21, 2.797633e+07, 3.455296e+00, -3.306761e-08, -2.062866e-22, -4.653724e+07, -3.694312e-17, 2.254095e-06, 3.519767e-16, 1.292737e-06, -3.840896e-08, -1.946825e-20, 2.639141e+18, 3.021503e+07, -1.834066e+18, 4.474920e-02, 3.005033e-20, -1.233782e-10, -3.260111e-08, 2.326419e-09, -2.298222e-19, 7.554873e+15, 2.378479e+19, -5.092127e-03, -4.724838e-07, 3.204184e+06, 2.713748e-12, 1.574309e-05, 6.622323e-01, -4.944461e-01, -1.559672e+19, -3.350494e+15, 2.467451e-14, -4.881873e+13, 1.031263e+15, -4.051814e+12, 1.418548e+07, 1.204368e+17, -4.113152e-02, -4.472069e+16, 4.896886e-14, 2.371633e+05, 3.543019e+04, -3.083516e-22, 1.041761e-09, -2.579812e-06, -2.937567e+09, -4.775349e-16])
        out[564]=out1
        return out

    @is_d5.setter
    def is_d5(self,value):
        if (len(value)!=1): raise Exception()
        in1=value[328]
        ca(in1.Dims,[10,20])
        ca(in1.Real,[2.792909e-01, 6.554477e+16, 4.240073e-13, -4.490109e+19, 5.410527e-22, -2.244599e+17, -2.656142e-02, -3.819500e+13, -7.086082e-02, 7.790729e-13, 3.375900e-12, -6.915692e+09, -2.900437e-18, 1.257280e+05, -3.810852e+15, -4.589554e-12, 2.670612e-14, 4.725686e+06, -3.018046e+07, 2.439452e+07, 2.726039e-07, -2.805143e+02, -1.870376e+03, 4.573047e-06, 1.904868e+19, -1.966383e+00, 3.426469e-11, -1.400396e+13, -1.724273e+09, -7.347198e+10, -4.081057e-12, -3.868203e+10, -2.686071e+13, -5.289107e+01, -5.574151e-09, -2.580185e-06, -8.222097e-21, -4.957833e-12, -2.491984e+03, -7.900042e+16, -4.809370e-11, -2.048332e-19, 4.984852e-21, 1.350023e+13, -4.492022e-11, -3.255594e+10, 1.495149e-09, -7.272628e+02, -4.236196e-04, 4.736990e-02, -4.030173e-11, 1.017371e+11, 1.124559e-09, 4.177431e-21, 1.026706e+06, -4.702729e-04, -2.633498e+18, -4.689724e+08, -2.593657e+05, 3.433194e-18, -1.977738e-13, -1.163773e+03, 3.424738e-20, 7.391132e-06, 1.364867e+12, -7.155727e+16, 3.078093e-21, -3.151787e-04, -4.715633e+06, 1.017894e+19, -1.121778e+14, -3.529769e-10, 4.530606e+19, 3.988296e-17, -3.469818e+06, 1.204304e+03, -1.404314e+15, -1.369871e+04, -2.796125e-03, -4.842068e-06, -2.639632e-03, 1.324740e+08, 1.440651e+07, -4.778885e+03, -4.643859e+06, 1.726955e-09, -8.160334e+05, 3.763238e+13, 1.391028e+02, -4.269393e+04, -2.698233e+02, -3.677556e+14, 1.070699e-17, 3.949376e+19, 4.503080e-06, 4.344496e-07, 1.714091e-19, -3.436426e+01, 4.914505e+15, -1.101617e+09, -1.899511e-04, 2.195951e-06, 2.402701e-12, 1.783431e-09, -7.329137e-08, 4.423889e+16, 2.812547e-19, -7.848554e+05, -3.635151e+13, 3.128605e-09, -2.858963e+08, 2.086065e-11, -2.544450e+12, 1.450579e+19, -1.508905e+13, 4.307174e+00, 1.038108e-05, 4.313281e-05, 3.647351e+05, 1.309105e-16, 4.180469e+13, -2.701332e-07, -4.033566e+14, -3.116748e-06, 2.342296e-07, 1.870335e-19, 2.312273e+01, -4.478923e+08, -4.854324e+09, 2.681828e+03, -4.280128e-01, -4.690703e-21, 3.853815e+16, 1.366639e+02, -2.944985e-11, -4.486958e-13, 3.017750e-11, 3.551437e-13, 2.263828e-12, -6.545014e-18, -7.552023e+12, 7.595238e+14, 2.810247e+12, 6.516008e+15, -3.035786e+14, 2.523040e+11, -3.766603e+09, 7.316287e+18, -2.147132e+17, 1.972210e+10, 2.906768e-13, 4.226577e-14, -2.640568e+17, 2.181408e+10, -1.043256e-08, -3.649181e+06, -2.776638e+18, 3.660147e-07, -1.415433e-17, -4.945127e-17, 2.655050e+01, -2.269828e+04, -2.585499e-01, -3.299965e+05, 3.707494e-18, -1.257923e-19, -1.321880e+14, -1.815888e-12, 9.366926e-09, 1.024923e-14, 4.494907e+04, -2.596971e-20, -3.403446e-12, 1.537084e+17, -3.850430e-17, -4.821759e+05, 4.255435e-20, -1.016978e-16, 1.430658e-09, -3.696861e-14, -4.427905e-19, -1.999724e-09, -3.489402e-06, -4.677864e-03, 1.246884e+13, -4.458271e-19, 3.551905e-04, -4.458221e-20, -3.472033e+01, -1.745714e+08, 4.396891e+03, 4.345767e+02, -1.800116e+05, -1.217318e+00, 3.605072e-08, 1.306109e-09, -2.798295e+16, 4.387728e-13, -3.284039e+11, 3.424124e+17])

    @property
    def is_d6(self):
        out={}
        out1=MultiDimArray([5, 10],[4.229153e+02, 3.406523e+03, -2.158208e+15, -7.464845e+07, -4.763504e+18, 6.777497e-20, -1.265130e+18, 2.145141e+12, -8.473642e-18, -3.780104e+17, -4.356069e+06, 1.199990e+04, -2.413259e+07, -2.609077e-12, -2.121030e-16, -1.224176e+09, -2.836294e-15, -1.975701e-18, 4.311314e-04, -4.932020e-20, -1.307735e-18, -4.000536e+02, -1.718325e+15, -3.493595e+05, 1.707089e+00, 4.416780e+01, -1.152954e-13, 8.396437e-02, -4.304750e+16, 1.154166e+02, -2.331328e-02, 4.821737e-04, 5.831989e-20, -6.887913e+06, -1.592772e+11, 4.730754e-19, 2.543760e-17, -5.864767e+14, 2.077122e-13, 2.801695e-12, -1.171678e+12, -8.854966e+18, -1.555508e-08, 3.589410e+11, -1.495443e-21, 2.876586e-06, -2.265460e-03, 2.544109e-03, 2.019117e-06, -6.458547e-21])
        out["testval1"]=out1
        return out
    @is_d6.setter
    def is_d6(self,value):
        if (len(value)!=1): return Exception()
        in1=value["testval2"]
        ca(in1.Dims,[8, 10])
        ca(in1.Real,[2.080438e+03, -2.901444e-01, 2.561452e+12, 6.760682e+14, -2.461568e-10, -4.811907e-20, 6.299564e+11, -2.660066e-19, 4.643316e+13, 3.292265e-13, 1.187460e+19, 3.054313e-07, 3.503026e-20, -1.465147e-08, 3.993039e-17, 2.469296e-10, -4.014504e+07, 1.810733e+17, -3.976509e-19, -9.166607e+15, 1.854678e+02, 2.884879e-12, -4.382521e+14, 3.064407e-05, -9.542195e+07, -3.938411e-13, -2.850416e-03, 3.042038e+14, 1.464437e-12, -1.550126e-06, 4.938341e+11, -3.517527e+19, 3.135793e+19, 1.380313e-14, -1.060961e+18, 2.833127e-10, -1.862230e+02, -2.232851e-05, 4.773548e-05, 3.746071e+13, -4.972451e+09, 4.553754e-14, -8.183438e+10, 3.739120e+18, -1.619189e+19, 4.644394e+08, -8.327578e-11, 4.080876e-02, -2.806082e-03, -1.595033e-06, 1.973067e+16, 2.989575e-07, -8.974247e+15, -4.204211e-03, 1.513025e-02, -4.604953e+03, 4.107290e+16, -3.631920e+12, -1.902472e+13, -4.186326e-14, 2.465135e+13, 5.060414e+12, 7.508582e+11, 3.233186e-14, -6.750005e+14, -9.467336e-16, 2.101440e+03, -1.162425e+08, 7.808216e+04, 4.356208e-19, -3.316834e+14, 3.299774e-19, -3.746431e-16, -3.971172e-07, 2.423744e+10, 1.542747e+17, 2.358704e-05, 4.201668e+17, -3.736856e+07, 3.585645e-07])

    @property
    def is_str1(self):
        return {23 : "Hello server"}
    @is_str1.setter
    def is_str1(self,value):
        if (len(value)!=1): raise Exception()
        if (value[24]!="Hello client"): raise Exception()

    @property
    def is_str2(self):
        return {"testval1": "Hello server"}
    @is_str2.setter
    def is_str2(self,value):
        if (len(value)!=1): raise Exception()
        if (value["testval2"]!="Hello client"): raise Exception()

    @property
    def is_struct1(self):
        out={}
        out1=RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2")
        out1.mydat=[-9.692618e+00, -1.944240e+03, -2.456327e+16, 4.673405e-20, 5.147581e-14, -3.773975e+15, 2.336430e-21, 1.597144e-18, -2.609059e-03, 3.557639e-21, -1.666575e-16, -4.242788e-07, 2.686206e+07, -3.200902e-05, -1.549754e-06, -3.010796e-12, 4.638418e+01, 2.664397e-14, -2.689174e+01, 4.564584e-21]
        out[748]=out1
        return out
    @is_struct1.setter
    def is_struct1(self,value):
        if (len(value)!=1): raise Exception()
        ca(value[372].mydat,[-2.101948e-07, -2.594836e-08, 2.515710e+01, -3.834127e-14, -3.088095e+06, -3.256612e-02, -1.855481e-19, 3.801916e+07, 2.145894e+09, 4.487676e+12, 1.351202e-02, -1.125124e-16, 1.369826e-20, -2.290673e+00, 1.786029e-20, -4.991515e+08, 4.006107e-10, -4.947871e-11, -2.737020e-08, 4.123759e-20])

    @property
    def is_struct2(self):
        out={}
        out1= RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2")
        out1.mydat=[-4.489570e+13, 9.574895e-05, 4.081711e+06, 5.612839e-18, -1.078604e+05, 3.658139e+08, -4.748975e+05, -2.606481e+01, 3.016739e+15, 3.174709e+19, -4.572549e+17, 1.980389e-04, -3.551911e-10, 3.598401e-07, 2.659416e-12, -3.606157e+06, 2.059674e+17, -9.362336e-20, -3.299256e+17, -2.245745e+16]
        out["testval1"]=out1
        return out
    @is_struct2.setter
    def is_struct2(self,value):
        if (len(value)!=1): raise Exception()
        ca(value["testval2"].mydat,[6.931327e-21, 4.527137e-02, 1.260822e-18, 3.592805e-12, 1.088317e-05, 3.305865e+03, -9.798828e-20, 1.497504e+18, -3.653592e+01, 1.473952e+10, -1.003612e-20, 1.302159e+18, -8.544326e+05, 1.038521e+16, -2.845746e-18, -3.899909e-04, 4.785560e-02, -7.203365e-12, -1.500022e-14, -1.892753e-17])

    @property
    def is_struct3(self):
        out=RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService2.ostruct2")
        out.a1=[-8.483090e-19, -4.401548e-08, 3.908118e+00, 2.063513e-18, 4.237047e+18, -1.124681e-16, 3.924541e-01, -2.184335e-10, -1.978950e+11, 1.586365e+18, 1.712393e+00, -6.314723e+00, 1.196777e-16, -2.748704e-08, -1.289967e+02, -4.051137e+17, -1.902860e+10, -2.070486e+08, 3.622651e+06, 1.315398e+17]
        return out
    @is_struct3.setter
    def is_struct3(self,value):
        ca(value.a1,[-2.426765e+05, -9.410735e+01, -1.667915e+12, -4.084240e-05, 3.199460e+03, 8.256717e-12, -4.772119e-11, -1.061407e-13, 2.759750e+02, -1.212549e+10, 7.012690e+15, 3.953354e+04, -2.617985e-07, 1.104408e-21, -3.889366e+00, 4.549493e+16, -1.376791e+15, -3.445205e-21, 2.137830e-14, 4.620179e+18])

    @property
    def var_num(self):
        return RobotRaconteurVarValue([-1680284833, -54562307, 732107275, 1470526962, -1389452949, 256801409, 261288152, 1728150828, 1322531658, -1640628174, 1036878614, 511108054, 2057847386, 288780916, 996595759],"int32[]")
    @var_num.setter
    def var_num(self,value):
        ca(value.data,[-1046369769, 1950632347, 1140727074, -1277424443, 163999900, 970815027, 545593183, 514305170, 1896372264, 1385916382])

    @property
    def var_str(self):
        return RobotRaconteurVarValue("Hello Client!","string")
    @var_str.setter
    def var_str(self,value):
        if(value.data!="Hello Server!"): raise Exception()

    @property
    def var_struct(self):
        out=RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2")
        out.mydat=[-9.052731e+13, 4.151705e-17, -4.004463e+19, -2.838274e+03, 9.983314e+12, 2.764122e+10, -1.131486e+03, 2.418899e+12, 1.323675e-05, -4.602174e+13, 2.717530e+01, 1.193887e-10, -4.137578e+16, -1.246990e-19, 4.244315e-18, -2.833005e-08, 1.956266e-04, 4.130129e-21, 1.641708e-11, -4.488158e-19]
        return RobotRaconteurVarValue(out,"RobotRaconteurTestService.teststruct2")
    @var_struct.setter
    def var_struct(self,value):
        ca(value.data.mydat,[-4.945426e-20, 1.763386e+13, 3.431578e-04, 4.411409e+17, -2.690201e+03, 3.025939e-10, -3.659846e+11, -4.780435e-10, -3.246816e+14, -1.815578e+04, 2.236455e+10, -4.639041e+14, 1.767930e+10, -1.636094e+05, -4.392462e-01, 2.225260e+04, -5.250245e+18, 8.755282e-12, 2.005819e-10, 2.702210e+04])

    @property
    def var_vector(self):
        out={}
        out[10]="Hello Client!"
        return RobotRaconteurVarValue(out,"string{int32}")
    @var_vector.setter
    def var_vector(self,value):
        if (len(value.data)!=1): raise Exception()
        if (value.data[11]!="Hello Server!"): raise Exception()

    @property
    def var_dictionary(self):
        out={}
        out["test1"]="Hello Client!"
        return RobotRaconteurVarValue(out,"string{string}")
    @var_dictionary.setter
    def var_dictionary(self,value):
        if (len(value.data)!=1): raise Exception()
        if (value.data["test2"]!="Hello Server!"): raise Exception()

    @property
    def var_multidimarray(self):
        return RobotRaconteurVarValue(MultiDimArray([5, 4],[-4.915597e-01, 3.892823e+00, 2.622325e+08, -7.150935e+04, 9.418756e+00, 3.633879e+18, 3.522383e-03, -4.989811e+05, 2.027383e-03, -3.153241e+12, -6.948245e-21, -3.198577e+14, 6.172905e+09, 3.849430e+15, 8.600383e+13, 4.079437e-17, 3.194775e+06, 4.222550e-18, 1.758122e+17, -1.018308e+03]),"double[*]")
    @var_multidimarray.setter
    def var_multidimarray(self,value):
        ca(value.data.Dims,[5, 4])
        ca(value.data.Real,[3.792953e+00, 2.968121e-17, -3.976413e-15, 4.392986e+19, 2.197463e+10, -2.627743e-14, -2.184665e+17, 1.972257e-17, 9.929684e-03, -3.096821e+17, 3.598051e+11, -6.266015e-18, 1.811985e-11, 2.815232e-07, 7.469467e-06, 6.141798e+13, 3.105763e+09, -1.697809e-10, -4.141707e-17, 4.391634e+13])

    @property
    def errtest(self):
        raise Exception()
    @errtest.setter
    def errtest(self,value):
        raise Exception()

    @property
    def nulltest(self):
        return None
    @nulltest.setter
    def nulltest(self,value):
        if (not value is None): raise Exception()

    #functions
    def func1(self):
        def func1_thread():
            try:
                time.sleep(1)
                self.ev1.fire()
            except:
                traceback.print_exc()
        thread.start_new(func1_thread, ())

    def func2(self, d1, d2):
        def func2_thread():
            try:
                time.sleep(1)
                s=RobotRaconteurNode.s.NewStructure("RobotRaconteurTestService.teststruct2")
                s.mydat=[d2]
                self.ev2.fire(d1,s)
            except:
                traceback.print_exc()
        thread.start_new(func2_thread, ())

    def func3(self, d1, d2):
        return d1+d2

    def meaning_of_life(self):
        return 42

    def func_errtest(self):
        raise Exception()

    #objrefs
    def get_o1(self):
        return self._o1, "RobotRaconteurTestService.sub1"

    def get_o2(self,ind):
        iind=int(ind)
        with self._o2_lock:
            if (not iind in self._o2):
                self._o2[iind]=sub1_impl()
                self._o2[iind].i_ind=iind
            return self._o2[iind],  "RobotRaconteurTestService.sub1"

    def get_o3(self,ind):
        iind=int(ind)
        with self._o3_lock:
            if (not iind in self._o3):
                self._o3[iind]=sub1_impl()
                self._o3[iind].i_ind=iind
            return self._o3[iind], "RobotRaconteurTestService.sub1"

    def get_o4(self,ind):
        iind=unicode(ind)
        with self._o4_lock:
            if (not iind in self._o4):
                self._o4[iind]=sub1_impl()
                self._o4[iind].s_ind=iind
            return self._o4[iind],  "RobotRaconteurTestService.sub1"

    def get_o5(self,ind):
        return self._o5,  "RobotRaconteurTestService.sub1"

    def get_o6(self):
        if (isinstance(self._o6,sub1_impl)):
            return self._o6,  "RobotRaconteurTestService.sub1"
        if (isinstance(self._o6,sub2_impl)):
            return self._o6, "RobotRaconteurTestService.sub2"
        if (isinstance(self._o6,subobj_impl)):
            return self._o6, "RobotRaconteurTestService2.subobj"

    def o6_op(self, op):
        try:
            #print "op " + ServerContext.GetCurrentServicePath() + ".o6"
            ServerContext.GetCurrentServerContext().ReleaseServicePath(ServerContext.GetCurrentServicePath() + ".o6")
        except:
            traceback.print_exc()

        if (op==0):
            self._o6=sub1_impl()
        elif (op==1):
            self._o6=sub2_impl()
        elif (op==2):
            self._o6=subobj_impl()
        else:
            raise Exception()

    #pipes
    @property
    def p1(self):
        return self._p1
    @p1.setter
    def p1(self,value):
        self._p1=value
        value.PipeConnectCallback=(self.p1_connect_callback)

    def p1_connect_callback(self,p):
        p.RequestPacketAck=True
        p.PacketReceivedEvent+=self.p1_packet_received
        p.PacketAckReceivedEvent+=self.p1_packet_ack_received

    def p1_packet_received(self,p):
        def p1_pr():

            time.sleep(.5)
            with self._p1_lock:
                while p.Available:
                    dat=p.ReceivePacket()
                    pnum=p.SendPacket(dat)
                    if (not self._packet_sent):
                        self._packetnum=pnum
                        self._packet_sent=True
        thread.start_new(p1_pr, ())

    def p1_packet_ack_received(self,p,packetnum):
        if (packetnum == self._packetnum):
            self._ack_recv=True


    @property
    def p2(self):
        return self._p2
    @p2.setter
    def p2(self,value):
        self._p2=value
        value.PipeConnectCallback=self.p2_connect_callback

    def p2_connect_callback(self,p):
        p.PacketReceivedEvent+=self.p2_packet_received

    def p2_packet_received(self,p):
        time.sleep(.5)
        with self._p2_lock:
            while p.Available > 0:
                dat=p.ReceivePacket()
                p.SendPacket(dat)


    def pipe_check_error(self):
        if (not self._ack_recv): raise Exception()

    #callbacks
    def test_callbacks(self):
        ep=ServerEndpoint.GetCurrentEndpoint()
        self.cb1.GetClientFunction(ep)()
        self.cb2.GetClientFunction(ep)(739.2,0.392)
        res=self.cb3.GetClientFunction(ep)(34,45)
        if (res != (34 + 45 + 3.14)): raise Exception()
        if (self.cb_meaning_of_life.GetClientFunction(ep)()!=42): raise Exception()

        errthrown=False
        try:
            self.cb_errtest.GetClientFunction(ep)()
        except:
            traceback.print_exc()
            errthrown=True

        if (not errthrown):
            raise Exception()
    #wires
    @property
    def w1(self):
        return self._w1
    @w1.setter
    def w1(self,value):
        self._w1=value
        value.WireConnectCallback=self.w1_connect_callback

    def w1_connect_callback(self,w):
        #print "connect"
        w.WireValueChanged+=self.w1_value_changed

    def w1_value_changed(self,w,value,time):
        #print "change"
        w.OutValue=w.InValue

    @property
    def w2(self):
        return self._w2
    @w2.setter
    def w2(self,value):
        self._w2=value
        value.WireConnectCallback=self.w2_connect_callback

    def w2_connect_callback(self,w):
        w.WireValueChanged+=self.w2_value_changed

    def w2_value_changed(self,w,value,time):
        w.OutValue=w.InValue

    @property
    def w3(self):
        return self._w1
    @w3.setter
    def w3(self,value):
        self._w3=value
        value.WireConnectCallback=self.w3_connect_callback

    def w3_connect_callback(self,w):
        w.WireValueChanged+=self.w3_value_changed

    def w3_value_changed(self,w,value,time):
        w.OutValue=w.InValue



class sub1_impl(object):
    def __init__(self):
        self.d1=None
        self.d2=None
        self.s_ind=""
        self.i_ind=0

        self._o2_1=sub2_impl()
        self._o2_2={}
        self._o2_2_lock=threading.RLock()
        self._o2_3={}
        self._o2_3_lock=threading.RLock()

        self._lock=threading.RLock()

    def RobotRaconteurMonitorEnter(self,timeout):
        print "Monitor enter"
        self._lock.acquire()

    def RobotRaconteurMonitorExit(self):
        print "Monitor exit"
        self._lock.release()

    def get_o2_1(self):
        return self._o2_1,  "RobotRaconteurTestService.sub2"

    def get_o2_2(self,ind):
        iind=int(ind)
        with self._o2_2_lock:
            if (not iind in self._o2_2):
                self._o2_2[iind]=sub2_impl()
                self._o2_2[iind].i_ind=iind
            return self._o2_2[iind],  "RobotRaconteurTestService.sub2"

    def get_o2_3(self,ind):
        iind=unicode(ind)
        with self._o2_3_lock:
            if (not iind in self._o2_3):
                self._o2_3[iind]=sub2_impl()
                self._o2_3[iind].s_ind=iind
            return self._o2_3[iind],  "RobotRaconteurTestService.sub2"

class sub2_impl(object):
    def __init__(self):
        self.s_ind=""
        self.i_ind=0
        self.data=""

        self._o3_1={}
        self._o3_1_lock=threading.RLock()

    def get_o3_1(self,ind):
        iind=unicode(ind)
        with self._o3_1_lock:
            if (not iind in self._o3_1):
                self._o3_1[iind]=sub3_impl()
                self._o3_1[iind].ind=iind
            return self._o3_1[iind],  "RobotRaconteurTestService.sub3"

class sub3_impl(object):
    def __init__(self):
        self.ind=""
        self.data2=""
        self.data3=0

    def add(self,d):
        return d+42

class subobj_impl(object):
    def add_val(self,v):
        return v+1


if __name__ == '__main__':
    main()
