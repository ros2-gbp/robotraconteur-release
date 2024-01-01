/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.1.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class TimeSpec {
  private transient long swigCPtr;
  protected transient boolean swigCMemOwn;

  protected TimeSpec(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(TimeSpec obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected static long swigRelease(TimeSpec obj) {
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
        RobotRaconteurJavaJNI.delete_TimeSpec(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  public void setSeconds(long value) {
    RobotRaconteurJavaJNI.TimeSpec_seconds_set(swigCPtr, this, value);
  }

  public long getSeconds() {
    return RobotRaconteurJavaJNI.TimeSpec_seconds_get(swigCPtr, this);
  }

  public void setNanoseconds(int value) {
    RobotRaconteurJavaJNI.TimeSpec_nanoseconds_set(swigCPtr, this, value);
  }

  public int getNanoseconds() {
    return RobotRaconteurJavaJNI.TimeSpec_nanoseconds_get(swigCPtr, this);
  }

  public TimeSpec() {
    this(RobotRaconteurJavaJNI.new_TimeSpec__SWIG_0(), true);
  }

  public TimeSpec(long seconds, int nanoseconds) {
    this(RobotRaconteurJavaJNI.new_TimeSpec__SWIG_1(seconds, nanoseconds), true);
  }

  public boolean equals(TimeSpec t2) {
    return RobotRaconteurJavaJNI.TimeSpec_equals(swigCPtr, this, TimeSpec.getCPtr(t2), t2);
  }

  public boolean ne(TimeSpec t2) {
    return RobotRaconteurJavaJNI.TimeSpec_ne(swigCPtr, this, TimeSpec.getCPtr(t2), t2);
  }

  public TimeSpec sub(TimeSpec t2) {
    return new TimeSpec(RobotRaconteurJavaJNI.TimeSpec_sub(swigCPtr, this, TimeSpec.getCPtr(t2), t2), true);
  }

  public TimeSpec add(TimeSpec t2) {
    return new TimeSpec(RobotRaconteurJavaJNI.TimeSpec_add(swigCPtr, this, TimeSpec.getCPtr(t2), t2), true);
  }

  public boolean gt(TimeSpec t2) {
    return RobotRaconteurJavaJNI.TimeSpec_gt(swigCPtr, this, TimeSpec.getCPtr(t2), t2);
  }

  public boolean ge(TimeSpec t2) {
    return RobotRaconteurJavaJNI.TimeSpec_ge(swigCPtr, this, TimeSpec.getCPtr(t2), t2);
  }

  public boolean lt(TimeSpec t2) {
    return RobotRaconteurJavaJNI.TimeSpec_lt(swigCPtr, this, TimeSpec.getCPtr(t2), t2);
  }

  public boolean le(TimeSpec t2) {
    return RobotRaconteurJavaJNI.TimeSpec_le(swigCPtr, this, TimeSpec.getCPtr(t2), t2);
  }

  public void cleanup_nanosecs() {
    RobotRaconteurJavaJNI.TimeSpec_cleanup_nanosecs(swigCPtr, this);
  }

}