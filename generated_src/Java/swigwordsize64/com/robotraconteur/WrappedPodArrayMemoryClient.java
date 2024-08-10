/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.2.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class WrappedPodArrayMemoryClient {
  private transient long swigCPtr;
  private transient boolean swigCMemOwn;

  protected WrappedPodArrayMemoryClient(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(WrappedPodArrayMemoryClient obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected void swigSetCMemOwn(boolean own) {
    swigCMemOwn = own;
  }

  @SuppressWarnings({"deprecation", "removal"})
  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if (swigCPtr != 0) {
      if (swigCMemOwn) {
        swigCMemOwn = false;
        RobotRaconteurJavaJNI.delete_WrappedPodArrayMemoryClient(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  public java.math.BigInteger length() {
    return RobotRaconteurJavaJNI.WrappedPodArrayMemoryClient_length(swigCPtr, this);
  }

  public MemberDefinition_Direction direction() {
    return MemberDefinition_Direction.swigToEnum(RobotRaconteurJavaJNI.WrappedPodArrayMemoryClient_direction(swigCPtr, this));
  }

  public void read(java.math.BigInteger memorypos, WrappedPodArrayMemoryClientBuffer buffer, java.math.BigInteger bufferpos, java.math.BigInteger count) {
    RobotRaconteurJavaJNI.WrappedPodArrayMemoryClient_read(swigCPtr, this, memorypos, WrappedPodArrayMemoryClientBuffer.getCPtr(buffer), buffer, bufferpos, count);
  }

  public void write(java.math.BigInteger memorypos, WrappedPodArrayMemoryClientBuffer buffer, java.math.BigInteger bufferpos, java.math.BigInteger count) {
    RobotRaconteurJavaJNI.WrappedPodArrayMemoryClient_write(swigCPtr, this, memorypos, WrappedPodArrayMemoryClientBuffer.getCPtr(buffer), buffer, bufferpos, count);
  }

}
