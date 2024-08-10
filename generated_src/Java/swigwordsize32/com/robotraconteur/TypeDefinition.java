/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.2.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class TypeDefinition {
  private transient long swigCPtr;
  private transient boolean swigCMemOwn;

  protected TypeDefinition(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(TypeDefinition obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected void swigSetCMemOwn(boolean own) {
    swigCMemOwn = own;
  }

  @SuppressWarnings({"deprecation", "removal"})
  protected void finalize() {
    delete();
  }

  public synchronized void delete() {
    if (swigCPtr != 0) {
      if (swigCMemOwn) {
        swigCMemOwn = false;
        RobotRaconteurJavaJNI.delete_TypeDefinition(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  public void setName(String value) {
    RobotRaconteurJavaJNI.TypeDefinition_Name_set(swigCPtr, this, value);
  }

  public String getName() {
    return RobotRaconteurJavaJNI.TypeDefinition_Name_get(swigCPtr, this);
  }

  public void setType(DataTypes value) {
    RobotRaconteurJavaJNI.TypeDefinition_Type_set(swigCPtr, this, value.swigValue());
  }

  public DataTypes getType() {
    return DataTypes.swigToEnum(RobotRaconteurJavaJNI.TypeDefinition_Type_get(swigCPtr, this));
  }

  public void setTypeString(String value) {
    RobotRaconteurJavaJNI.TypeDefinition_TypeString_set(swigCPtr, this, value);
  }

  public String getTypeString() {
    return RobotRaconteurJavaJNI.TypeDefinition_TypeString_get(swigCPtr, this);
  }

  public void setArrayType(DataTypes_ArrayTypes value) {
    RobotRaconteurJavaJNI.TypeDefinition_ArrayType_set(swigCPtr, this, value.swigValue());
  }

  public DataTypes_ArrayTypes getArrayType() {
    return DataTypes_ArrayTypes.swigToEnum(RobotRaconteurJavaJNI.TypeDefinition_ArrayType_get(swigCPtr, this));
  }

  public void setArrayVarLength(boolean value) {
    RobotRaconteurJavaJNI.TypeDefinition_ArrayVarLength_set(swigCPtr, this, value);
  }

  public boolean getArrayVarLength() {
    return RobotRaconteurJavaJNI.TypeDefinition_ArrayVarLength_get(swigCPtr, this);
  }

  public void setArrayLength(vectorint32 value) {
    RobotRaconteurJavaJNI.TypeDefinition_ArrayLength_set(swigCPtr, this, vectorint32.getCPtr(value), value);
  }

  public vectorint32 getArrayLength() {
    long cPtr = RobotRaconteurJavaJNI.TypeDefinition_ArrayLength_get(swigCPtr, this);
    return (cPtr == 0) ? null : new vectorint32(cPtr, false);
  }

  public void setContainerType(DataTypes_ContainerTypes value) {
    RobotRaconteurJavaJNI.TypeDefinition_ContainerType_set(swigCPtr, this, value.swigValue());
  }

  public DataTypes_ContainerTypes getContainerType() {
    return DataTypes_ContainerTypes.swigToEnum(RobotRaconteurJavaJNI.TypeDefinition_ContainerType_get(swigCPtr, this));
  }

  public TypeDefinition() {
    this(RobotRaconteurJavaJNI.new_TypeDefinition__SWIG_0(), true);
  }

  public String toString() {
    return RobotRaconteurJavaJNI.TypeDefinition_toString(swigCPtr, this);
  }

  public void fromString(String s, ServiceDefinitionParseInfo parse_info) {
    RobotRaconteurJavaJNI.TypeDefinition_fromString__SWIG_0(swigCPtr, this, s, ServiceDefinitionParseInfo.getCPtr(parse_info), parse_info);
  }

  public void fromString(String s) {
    RobotRaconteurJavaJNI.TypeDefinition_fromString__SWIG_1(swigCPtr, this, s);
  }

  public static DataTypes dataTypeFromString(String d) {
    return DataTypes.swigToEnum(RobotRaconteurJavaJNI.TypeDefinition_dataTypeFromString(d));
  }

  public static String stringFromDataType(DataTypes d) {
    return RobotRaconteurJavaJNI.TypeDefinition_stringFromDataType(d.swigValue());
  }

  public MemberDefinition getMember() {
    long cPtr = RobotRaconteurJavaJNI.TypeDefinition_getMember(swigCPtr, this);
    return (cPtr == 0) ? null : new MemberDefinition(cPtr, true);
  }

  public void setMember(MemberDefinition value) {
    RobotRaconteurJavaJNI.TypeDefinition_setMember(swigCPtr, this, MemberDefinition.getCPtr(value), value);
  }

  public void copyTo(TypeDefinition def) {
    RobotRaconteurJavaJNI.TypeDefinition_copyTo(swigCPtr, this, TypeDefinition.getCPtr(def), def);
  }

  public TypeDefinition clone() {
    long cPtr = RobotRaconteurJavaJNI.TypeDefinition_clone(swigCPtr, this);
    return (cPtr == 0) ? null : new TypeDefinition(cPtr, true);
  }

  public void rename(String name) {
    RobotRaconteurJavaJNI.TypeDefinition_rename(swigCPtr, this, name);
  }

  public void removeContainers() {
    RobotRaconteurJavaJNI.TypeDefinition_removeContainers(swigCPtr, this);
  }

  public void removeArray() {
    RobotRaconteurJavaJNI.TypeDefinition_removeArray(swigCPtr, this);
  }

  public void qualifyTypeStringWithUsing() {
    RobotRaconteurJavaJNI.TypeDefinition_qualifyTypeStringWithUsing(swigCPtr, this);
  }

  public void unqualifyTypeStringWithUsing() {
    RobotRaconteurJavaJNI.TypeDefinition_unqualifyTypeStringWithUsing(swigCPtr, this);
  }

  public void reset() {
    RobotRaconteurJavaJNI.TypeDefinition_reset(swigCPtr, this);
  }

  public TypeDefinition(TypeDefinition other) {
    this(RobotRaconteurJavaJNI.new_TypeDefinition__SWIG_1(TypeDefinition.getCPtr(other), other), true);
  }

}
