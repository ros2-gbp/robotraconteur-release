/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.2.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class RRBaseArray extends MessageElementData {
  private transient long swigCPtr;
  private transient boolean swigCMemOwnDerived;

  protected RRBaseArray(long cPtr, boolean cMemoryOwn) {
    super(RobotRaconteurJavaJNI.RRBaseArray_SWIGSmartPtrUpcast(cPtr), true);
    swigCMemOwnDerived = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(RRBaseArray obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  @SuppressWarnings({"deprecation", "removal"})
  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if(swigCPtr != 0 && swigCMemOwnDerived) {
      swigCMemOwnDerived = false;
      RobotRaconteurJavaJNI.delete_RRBaseArray(swigCPtr);
    }
    swigCPtr = 0;
    super.delete();
  }

  public String getTypeString() {
    return RobotRaconteurJavaJNI.RRBaseArray_getTypeString(swigCPtr, this);
  }

  public long size() {
    return RobotRaconteurJavaJNI.RRBaseArray_size(swigCPtr, this);
  }

  public SWIGTYPE_p_void void_ptr() {
    long cPtr = RobotRaconteurJavaJNI.RRBaseArray_void_ptr(swigCPtr, this);
    return (cPtr == 0) ? null : new SWIGTYPE_p_void(cPtr, false);
  }

  public long elementSize() {
    return RobotRaconteurJavaJNI.RRBaseArray_elementSize(swigCPtr, this);
  }

  public DataTypes getTypeID() {
    return DataTypes.swigToEnum(RobotRaconteurJavaJNI.RRBaseArray_getTypeID(swigCPtr, this));
  }

}
