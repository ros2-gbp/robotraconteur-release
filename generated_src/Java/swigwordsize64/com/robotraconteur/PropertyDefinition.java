/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 4.0.2
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class PropertyDefinition extends MemberDefinition {
  private transient long swigCPtr;
  private transient boolean swigCMemOwnDerived;

  protected PropertyDefinition(long cPtr, boolean cMemoryOwn) {
    super(RobotRaconteurJavaJNI.PropertyDefinition_SWIGSmartPtrUpcast(cPtr), true);
    swigCMemOwnDerived = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(PropertyDefinition obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected void swigSetCMemOwn(boolean own) {
    swigCMemOwnDerived = own;
    super.swigSetCMemOwn(own);
  }

  @SuppressWarnings("deprecation")
  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if (swigCPtr != 0) {
      if (swigCMemOwnDerived) {
        swigCMemOwnDerived = false;
        RobotRaconteurJavaJNI.delete_PropertyDefinition(swigCPtr);
      }
      swigCPtr = 0;
    }
    super.delete();
  }

  public void setType(TypeDefinition value) {
    RobotRaconteurJavaJNI.PropertyDefinition_Type_set(swigCPtr, this, TypeDefinition.getCPtr(value), value);
  }

  public TypeDefinition getType() {
    long cPtr = RobotRaconteurJavaJNI.PropertyDefinition_Type_get(swigCPtr, this);
    return (cPtr == 0) ? null : new TypeDefinition(cPtr, true);
  }

  public PropertyDefinition(ServiceEntryDefinition ServiceEntry) {
    this(RobotRaconteurJavaJNI.new_PropertyDefinition(ServiceEntryDefinition.getCPtr(ServiceEntry), ServiceEntry), true);
  }

  public String toString() {
    return RobotRaconteurJavaJNI.PropertyDefinition_toString__SWIG_0(swigCPtr, this);
  }

  public String toString(boolean isstruct) {
    return RobotRaconteurJavaJNI.PropertyDefinition_toString__SWIG_1(swigCPtr, this, isstruct);
  }

  public void fromString(String s, ServiceDefinitionParseInfo parse_info) {
    RobotRaconteurJavaJNI.PropertyDefinition_fromString__SWIG_0(swigCPtr, this, s, ServiceDefinitionParseInfo.getCPtr(parse_info), parse_info);
  }

  public void fromString(String s) {
    RobotRaconteurJavaJNI.PropertyDefinition_fromString__SWIG_1(swigCPtr, this, s);
  }

}