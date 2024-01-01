/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.1.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class vectorstring extends java.util.AbstractList<String> implements java.util.RandomAccess {
  private transient long swigCPtr;
  protected transient boolean swigCMemOwn;

  protected vectorstring(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(vectorstring obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected static long swigRelease(vectorstring obj) {
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
        RobotRaconteurJavaJNI.delete_vectorstring(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  public vectorstring(String[] initialElements) {
    this();
    reserve(initialElements.length);

    for (String element : initialElements) {
      add(element);
    }
  }

  public vectorstring(Iterable<String> initialElements) {
    this();
    for (String element : initialElements) {
      add(element);
    }
  }

  public String get(int index) {
    return doGet(index);
  }

  public String set(int index, String e) {
    return doSet(index, e);
  }

  public boolean add(String e) {
    modCount++;
    doAdd(e);
    return true;
  }

  public void add(int index, String e) {
    modCount++;
    doAdd(index, e);
  }

  public String remove(int index) {
    modCount++;
    return doRemove(index);
  }

  protected void removeRange(int fromIndex, int toIndex) {
    modCount++;
    doRemoveRange(fromIndex, toIndex);
  }

  public int size() {
    return doSize();
  }

  public vectorstring() {
    this(RobotRaconteurJavaJNI.new_vectorstring__SWIG_0(), true);
  }

  public vectorstring(vectorstring other) {
    this(RobotRaconteurJavaJNI.new_vectorstring__SWIG_1(vectorstring.getCPtr(other), other), true);
  }

  public long capacity() {
    return RobotRaconteurJavaJNI.vectorstring_capacity(swigCPtr, this);
  }

  public void reserve(long n) {
    RobotRaconteurJavaJNI.vectorstring_reserve(swigCPtr, this, n);
  }

  public boolean isEmpty() {
    return RobotRaconteurJavaJNI.vectorstring_isEmpty(swigCPtr, this);
  }

  public void clear() {
    RobotRaconteurJavaJNI.vectorstring_clear(swigCPtr, this);
  }

  public vectorstring(int count, String value) {
    this(RobotRaconteurJavaJNI.new_vectorstring__SWIG_2(count, value), true);
  }

  private int doSize() {
    return RobotRaconteurJavaJNI.vectorstring_doSize(swigCPtr, this);
  }

  private void doAdd(String x) {
    RobotRaconteurJavaJNI.vectorstring_doAdd__SWIG_0(swigCPtr, this, x);
  }

  private void doAdd(int index, String x) {
    RobotRaconteurJavaJNI.vectorstring_doAdd__SWIG_1(swigCPtr, this, index, x);
  }

  private String doRemove(int index) {
    return RobotRaconteurJavaJNI.vectorstring_doRemove(swigCPtr, this, index);
  }

  private String doGet(int index) {
    return RobotRaconteurJavaJNI.vectorstring_doGet(swigCPtr, this, index);
  }

  private String doSet(int index, String val) {
    return RobotRaconteurJavaJNI.vectorstring_doSet(swigCPtr, this, index, val);
  }

  private void doRemoveRange(int fromIndex, int toIndex) {
    RobotRaconteurJavaJNI.vectorstring_doRemoveRange(swigCPtr, this, fromIndex, toIndex);
  }

}