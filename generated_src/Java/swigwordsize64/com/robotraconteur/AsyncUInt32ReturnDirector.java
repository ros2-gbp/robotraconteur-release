/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 4.0.2
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class AsyncUInt32ReturnDirector {
  private transient long swigCPtr;
  protected transient boolean swigCMemOwn;

  protected AsyncUInt32ReturnDirector(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(AsyncUInt32ReturnDirector obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  @SuppressWarnings("deprecation")
  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if (swigCPtr != 0) {
      if (swigCMemOwn) {
        swigCMemOwn = false;
        RobotRaconteurJavaJNI.delete_AsyncUInt32ReturnDirector(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  protected void swigDirectorDisconnect() {
    swigCMemOwn = false;
    delete();
  }

  public void swigReleaseOwnership() {
    swigCMemOwn = false;
    RobotRaconteurJavaJNI.AsyncUInt32ReturnDirector_change_ownership(this, swigCPtr, false);
  }

  public void swigTakeOwnership() {
    swigCMemOwn = true;
    RobotRaconteurJavaJNI.AsyncUInt32ReturnDirector_change_ownership(this, swigCPtr, true);
  }

  public void handler(long ret, HandlerErrorInfo error) {
    RobotRaconteurJavaJNI.AsyncUInt32ReturnDirector_handler(swigCPtr, this, ret, HandlerErrorInfo.getCPtr(error), error);
  }

  public AsyncUInt32ReturnDirector() {
    this(RobotRaconteurJavaJNI.new_AsyncUInt32ReturnDirector(), true);
    RobotRaconteurJavaJNI.AsyncUInt32ReturnDirector_director_connect(this, swigCPtr, true, true);
  }

}