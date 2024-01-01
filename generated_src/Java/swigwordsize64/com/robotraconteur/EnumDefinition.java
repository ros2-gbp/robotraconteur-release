/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 4.0.2
 *
 * Do not make changes to this file unless you know what you are doing--modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class EnumDefinition {
  private transient long swigCPtr;
  private transient boolean swigCMemOwn;

  protected EnumDefinition(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(EnumDefinition obj) {
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
        RobotRaconteurJavaJNI.delete_EnumDefinition(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  public void setName(String value) {
    RobotRaconteurJavaJNI.EnumDefinition_Name_set(swigCPtr, this, value);
  }

  public String getName() {
    return RobotRaconteurJavaJNI.EnumDefinition_Name_get(swigCPtr, this);
  }

  public void setDocString(String value) {
    RobotRaconteurJavaJNI.EnumDefinition_DocString_set(swigCPtr, this, value);
  }

  public String getDocString() {
    return RobotRaconteurJavaJNI.EnumDefinition_DocString_get(swigCPtr, this);
  }

  public void setValues(vector_enumdefinitionvalues value) {
    RobotRaconteurJavaJNI.EnumDefinition_Values_set(swigCPtr, this, vector_enumdefinitionvalues.getCPtr(value), value);
  }

  public vector_enumdefinitionvalues getValues() {
    long cPtr = RobotRaconteurJavaJNI.EnumDefinition_Values_get(swigCPtr, this);
    return (cPtr == 0) ? null : new vector_enumdefinitionvalues(cPtr, false);
  }

  public void setParseInfo(ServiceDefinitionParseInfo value) {
    RobotRaconteurJavaJNI.EnumDefinition_ParseInfo_set(swigCPtr, this, ServiceDefinitionParseInfo.getCPtr(value), value);
  }

  public ServiceDefinitionParseInfo getParseInfo() {
    long cPtr = RobotRaconteurJavaJNI.EnumDefinition_ParseInfo_get(swigCPtr, this);
    return (cPtr == 0) ? null : new ServiceDefinitionParseInfo(cPtr, false);
  }

  public ServiceDefinition getService() {
    long cPtr = RobotRaconteurJavaJNI.EnumDefinition_getService(swigCPtr, this);
    return (cPtr == 0) ? null : new ServiceDefinition(cPtr, true);
  }

  public void setService(ServiceDefinition value) {
    RobotRaconteurJavaJNI.EnumDefinition_setService(swigCPtr, this, ServiceDefinition.getCPtr(value), value);
  }

  public EnumDefinition(ServiceDefinition service) {
    this(RobotRaconteurJavaJNI.new_EnumDefinition(ServiceDefinition.getCPtr(service), service), true);
  }

  public String toString() {
    return RobotRaconteurJavaJNI.EnumDefinition_toString(swigCPtr, this);
  }

  public void fromString(String s, ServiceDefinitionParseInfo parse_info) {
    RobotRaconteurJavaJNI.EnumDefinition_fromString__SWIG_0(swigCPtr, this, s, ServiceDefinitionParseInfo.getCPtr(parse_info), parse_info);
  }

  public void fromString(String s) {
    RobotRaconteurJavaJNI.EnumDefinition_fromString__SWIG_1(swigCPtr, this, s);
  }

  public boolean verifyValues() {
    return RobotRaconteurJavaJNI.EnumDefinition_verifyValues(swigCPtr, this);
  }

  public void reset() {
    RobotRaconteurJavaJNI.EnumDefinition_reset(swigCPtr, this);
  }

}