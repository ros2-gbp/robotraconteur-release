/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.1.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

class WallTimer_initstruct {
  private transient long swigCPtr;
  protected transient boolean swigCMemOwn;

  protected WallTimer_initstruct(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(WallTimer_initstruct obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected static long swigRelease(WallTimer_initstruct obj) {
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
        RobotRaconteurJavaJNI.delete_WallTimer_initstruct(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  public void setHandler(AsyncTimerEventReturnDirector value) {
    RobotRaconteurJavaJNI.WallTimer_initstruct_handler_set(swigCPtr, this, AsyncTimerEventReturnDirector.getCPtr(value), value);
  }

  public AsyncTimerEventReturnDirector getHandler() {
    long cPtr = RobotRaconteurJavaJNI.WallTimer_initstruct_handler_get(swigCPtr, this);
    return (cPtr == 0) ? null : new AsyncTimerEventReturnDirector(cPtr, false);
  }

  public void setId(int value) {
    RobotRaconteurJavaJNI.WallTimer_initstruct_id_set(swigCPtr, this, value);
  }

  public int getId() {
    return RobotRaconteurJavaJNI.WallTimer_initstruct_id_get(swigCPtr, this);
  }

  public WallTimer_initstruct() {
    this(RobotRaconteurJavaJNI.new_WallTimer_initstruct(), true);
  }

}