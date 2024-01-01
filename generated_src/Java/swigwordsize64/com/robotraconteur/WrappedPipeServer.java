/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.1.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class WrappedPipeServer {
  private transient long swigCPtr;
  private transient boolean swigCMemOwn;

  protected WrappedPipeServer(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(WrappedPipeServer obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected void swigSetCMemOwn(boolean own) {
    swigCMemOwn = own;
  }

  @SuppressWarnings("deprecation")
  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if (swigCPtr != 0) {
      if (swigCMemOwn) {
        swigCMemOwn = false;
        RobotRaconteurJavaJNI.delete_WrappedPipeServer(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  public String getMemberName() {
    return RobotRaconteurJavaJNI.WrappedPipeServer_getMemberName(swigCPtr, this);
  }

  public void setType(TypeDefinition value) {
    RobotRaconteurJavaJNI.WrappedPipeServer_Type_set(swigCPtr, this, TypeDefinition.getCPtr(value), value);
  }

  public TypeDefinition getType() {
    long cPtr = RobotRaconteurJavaJNI.WrappedPipeServer_Type_get(swigCPtr, this);
    return (cPtr == 0) ? null : new TypeDefinition(cPtr, true);
  }

  public void setWrappedPipeConnectCallback(WrappedPipeServerConnectDirector director, int id) {
    RobotRaconteurJavaJNI.WrappedPipeServer_setWrappedPipeConnectCallback(swigCPtr, this, WrappedPipeServerConnectDirector.getCPtr(director), director, id);
  }

  public RobotRaconteurNode getNode() {
    long cPtr = RobotRaconteurJavaJNI.WrappedPipeServer_getNode(swigCPtr, this);
    return (cPtr == 0) ? null : new RobotRaconteurNode(cPtr, true);
  }

  public MemberDefinition_Direction direction() {
    return MemberDefinition_Direction.swigToEnum(RobotRaconteurJavaJNI.WrappedPipeServer_direction(swigCPtr, this));
  }

}