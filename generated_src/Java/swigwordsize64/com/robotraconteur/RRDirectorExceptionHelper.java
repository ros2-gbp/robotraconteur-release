/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 4.0.2
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class RRDirectorExceptionHelper {
  private transient long swigCPtr;
  protected transient boolean swigCMemOwn;

  protected RRDirectorExceptionHelper(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(RRDirectorExceptionHelper obj) {
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
        RobotRaconteurJavaJNI.delete_RRDirectorExceptionHelper(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

public static String exceptionToStackTraceString(Exception exp)
{
	java.io.StringWriter sw = new java.io.StringWriter();
	java.io.PrintWriter pw = new java.io.PrintWriter(sw);
	exp.printStackTrace(pw);
	return sw.toString();
}

  public static void reset() {
    RobotRaconteurJavaJNI.RRDirectorExceptionHelper_reset();
  }

  public static void setError(MessageEntry err, String exception_str) {
    RobotRaconteurJavaJNI.RRDirectorExceptionHelper_setError(MessageEntry.getCPtr(err), err, exception_str);
  }

  public static boolean isErrorPending() {
    return RobotRaconteurJavaJNI.RRDirectorExceptionHelper_isErrorPending();
  }

  public static MessageEntry getError() {
    long cPtr = RobotRaconteurJavaJNI.RRDirectorExceptionHelper_getError();
    return (cPtr == 0) ? null : new MessageEntry(cPtr, true);
  }

  public RRDirectorExceptionHelper() {
    this(RobotRaconteurJavaJNI.new_RRDirectorExceptionHelper(), true);
  }

}
