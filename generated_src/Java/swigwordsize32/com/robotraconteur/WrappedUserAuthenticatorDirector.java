/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.2.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class WrappedUserAuthenticatorDirector {
  private transient long swigCPtr;
  protected transient boolean swigCMemOwn;

  protected WrappedUserAuthenticatorDirector(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(WrappedUserAuthenticatorDirector obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected static long swigRelease(WrappedUserAuthenticatorDirector obj) {
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

  @SuppressWarnings({"deprecation", "removal"})
  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if (swigCPtr != 0) {
      if (swigCMemOwn) {
        swigCMemOwn = false;
        RobotRaconteurJavaJNI.delete_WrappedUserAuthenticatorDirector(swigCPtr);
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
    RobotRaconteurJavaJNI.WrappedUserAuthenticatorDirector_change_ownership(this, swigCPtr, false);
  }

  public void swigTakeOwnership() {
    swigCMemOwn = true;
    RobotRaconteurJavaJNI.WrappedUserAuthenticatorDirector_change_ownership(this, swigCPtr, true);
  }

  public AuthenticatedUser authenticateUser(String username, MessageElement credentials, ServerContext context) {
    long cPtr = RobotRaconteurJavaJNI.WrappedUserAuthenticatorDirector_authenticateUser(swigCPtr, this, username, MessageElement.getCPtr(credentials), credentials, ServerContext.getCPtr(context), context);
    return (cPtr == 0) ? null : new AuthenticatedUser(cPtr, true);
  }

  public WrappedUserAuthenticatorDirector() {
    this(RobotRaconteurJavaJNI.new_WrappedUserAuthenticatorDirector(), true);
    RobotRaconteurJavaJNI.WrappedUserAuthenticatorDirector_director_connect(this, swigCPtr, true, true);
  }

}
