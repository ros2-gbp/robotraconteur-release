/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 4.0.2
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class WrappedServiceSubscriptionFilterPredicateDirector {
  private transient long swigCPtr;
  protected transient boolean swigCMemOwn;

  protected WrappedServiceSubscriptionFilterPredicateDirector(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(WrappedServiceSubscriptionFilterPredicateDirector obj) {
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
        RobotRaconteurJavaJNI.delete_WrappedServiceSubscriptionFilterPredicateDirector(swigCPtr);
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
    RobotRaconteurJavaJNI.WrappedServiceSubscriptionFilterPredicateDirector_change_ownership(this, swigCPtr, false);
  }

  public void swigTakeOwnership() {
    swigCMemOwn = true;
    RobotRaconteurJavaJNI.WrappedServiceSubscriptionFilterPredicateDirector_change_ownership(this, swigCPtr, true);
  }

  public boolean predicate(ServiceInfo2Wrapped info) {
    return RobotRaconteurJavaJNI.WrappedServiceSubscriptionFilterPredicateDirector_predicate(swigCPtr, this, ServiceInfo2Wrapped.getCPtr(info), info);
  }

  public WrappedServiceSubscriptionFilterPredicateDirector() {
    this(RobotRaconteurJavaJNI.new_WrappedServiceSubscriptionFilterPredicateDirector(), true);
    RobotRaconteurJavaJNI.WrappedServiceSubscriptionFilterPredicateDirector_director_connect(this, swigCPtr, true, true);
  }

}