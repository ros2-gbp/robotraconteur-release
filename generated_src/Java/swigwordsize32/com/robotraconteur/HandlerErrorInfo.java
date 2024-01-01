/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.1.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class HandlerErrorInfo {
  private transient long swigCPtr;
  protected transient boolean swigCMemOwn;

  protected HandlerErrorInfo(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(HandlerErrorInfo obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected static long swigRelease(HandlerErrorInfo obj) {
    long ptr = 0;
    if (obj != null) {
      if (!obj.swigCMemOwn)
        throw new RuntimeException("Cannot release ownership as memory is not owned");
      ptr = obj.swigCPtr;
      obj.swigCMemOwn = false;
      obj.delete();
    }
    return ptr;
  }

  @SuppressWarnings("deprecation")
  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if (swigCPtr != 0) {
      if (swigCMemOwn) {
        swigCMemOwn = false;
        RobotRaconteurJavaJNI.delete_HandlerErrorInfo(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  public void setError_code(long value) {
    RobotRaconteurJavaJNI.HandlerErrorInfo_error_code_set(swigCPtr, this, value);
  }

  public long getError_code() {
    return RobotRaconteurJavaJNI.HandlerErrorInfo_error_code_get(swigCPtr, this);
  }

  public void setErrorname(String value) {
    RobotRaconteurJavaJNI.HandlerErrorInfo_errorname_set(swigCPtr, this, value);
  }

  public String getErrorname() {
    return RobotRaconteurJavaJNI.HandlerErrorInfo_errorname_get(swigCPtr, this);
  }

  public void setErrormessage(String value) {
    RobotRaconteurJavaJNI.HandlerErrorInfo_errormessage_set(swigCPtr, this, value);
  }

  public String getErrormessage() {
    return RobotRaconteurJavaJNI.HandlerErrorInfo_errormessage_get(swigCPtr, this);
  }

  public void setErrorsubname(String value) {
    RobotRaconteurJavaJNI.HandlerErrorInfo_errorsubname_set(swigCPtr, this, value);
  }

  public String getErrorsubname() {
    return RobotRaconteurJavaJNI.HandlerErrorInfo_errorsubname_get(swigCPtr, this);
  }

  public void setParam_(MessageElement value) {
    RobotRaconteurJavaJNI.HandlerErrorInfo_param__set(swigCPtr, this, MessageElement.getCPtr(value), value);
  }

  public MessageElement getParam_() {
    long cPtr = RobotRaconteurJavaJNI.HandlerErrorInfo_param__get(swigCPtr, this);
    return (cPtr == 0) ? null : new MessageElement(cPtr, true);
  }

  public HandlerErrorInfo() {
    this(RobotRaconteurJavaJNI.new_HandlerErrorInfo(), true);
  }

}