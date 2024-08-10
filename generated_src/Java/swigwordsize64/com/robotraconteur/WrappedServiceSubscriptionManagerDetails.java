/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.2.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.robotraconteur;

public class WrappedServiceSubscriptionManagerDetails {
  private transient long swigCPtr;
  protected transient boolean swigCMemOwn;

  protected WrappedServiceSubscriptionManagerDetails(long cPtr, boolean cMemoryOwn) {
    swigCMemOwn = cMemoryOwn;
    swigCPtr = cPtr;
  }

  protected static long getCPtr(WrappedServiceSubscriptionManagerDetails obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }

  protected static long swigRelease(WrappedServiceSubscriptionManagerDetails obj) {
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
        RobotRaconteurJavaJNI.delete_WrappedServiceSubscriptionManagerDetails(swigCPtr);
      }
      swigCPtr = 0;
    }
  }

  public void setName(String value) {
    RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_Name_set(swigCPtr, this, value);
  }

  public String getName() {
    return RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_Name_get(swigCPtr, this);
  }

  public void setConnectionMethod(ServiceSubscriptionManager_CONNECTION_METHOD value) {
    RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_ConnectionMethod_set(swigCPtr, this, value.swigValue());
  }

  public ServiceSubscriptionManager_CONNECTION_METHOD getConnectionMethod() {
    return ServiceSubscriptionManager_CONNECTION_METHOD.swigToEnum(RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_ConnectionMethod_get(swigCPtr, this));
  }

  public void setUrls(vectorstring value) {
    RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_Urls_set(swigCPtr, this, vectorstring.getCPtr(value), value);
  }

  public vectorstring getUrls() {
    long cPtr = RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_Urls_get(swigCPtr, this);
    return (cPtr == 0) ? null : new vectorstring(cPtr, false);
  }

  public void setUrlUsername(String value) {
    RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_UrlUsername_set(swigCPtr, this, value);
  }

  public String getUrlUsername() {
    return RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_UrlUsername_get(swigCPtr, this);
  }

  public void setUrlCredentials(MessageElementData value) {
    RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_UrlCredentials_set(swigCPtr, this, MessageElementData.getCPtr(value), value);
  }

  public MessageElementData getUrlCredentials() {
    long cPtr = RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_UrlCredentials_get(swigCPtr, this);
    return (cPtr == 0) ? null : new MessageElementData(cPtr, true);
  }

  public void setServiceTypes(vectorstring value) {
    RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_ServiceTypes_set(swigCPtr, this, vectorstring.getCPtr(value), value);
  }

  public vectorstring getServiceTypes() {
    long cPtr = RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_ServiceTypes_get(swigCPtr, this);
    return (cPtr == 0) ? null : new vectorstring(cPtr, false);
  }

  public void setFilter(WrappedServiceSubscriptionFilter value) {
    RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_Filter_set(swigCPtr, this, WrappedServiceSubscriptionFilter.getCPtr(value), value);
  }

  public WrappedServiceSubscriptionFilter getFilter() {
    long cPtr = RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_Filter_get(swigCPtr, this);
    return (cPtr == 0) ? null : new WrappedServiceSubscriptionFilter(cPtr, true);
  }

  public void setEnabled(boolean value) {
    RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_Enabled_set(swigCPtr, this, value);
  }

  public boolean getEnabled() {
    return RobotRaconteurJavaJNI.WrappedServiceSubscriptionManagerDetails_Enabled_get(swigCPtr, this);
  }

  public WrappedServiceSubscriptionManagerDetails() {
    this(RobotRaconteurJavaJNI.new_WrappedServiceSubscriptionManagerDetails__SWIG_0(), true);
  }

  public WrappedServiceSubscriptionManagerDetails(String Name, ServiceSubscriptionManager_CONNECTION_METHOD Connection_method, vectorstring Urls, String UrlUsername, MessageElementData UrlCredentials, vectorstring ServiceTypes, WrappedServiceSubscriptionFilter Filter, boolean Enabled) {
    this(RobotRaconteurJavaJNI.new_WrappedServiceSubscriptionManagerDetails__SWIG_1(Name, Connection_method.swigValue(), vectorstring.getCPtr(Urls), Urls, UrlUsername, MessageElementData.getCPtr(UrlCredentials), UrlCredentials, vectorstring.getCPtr(ServiceTypes), ServiceTypes, WrappedServiceSubscriptionFilter.getCPtr(Filter), Filter, Enabled), true);
  }

  public WrappedServiceSubscriptionManagerDetails(String Name, ServiceSubscriptionManager_CONNECTION_METHOD Connection_method, vectorstring Urls, String UrlUsername, MessageElementData UrlCredentials, vectorstring ServiceTypes, WrappedServiceSubscriptionFilter Filter) {
    this(RobotRaconteurJavaJNI.new_WrappedServiceSubscriptionManagerDetails__SWIG_2(Name, Connection_method.swigValue(), vectorstring.getCPtr(Urls), Urls, UrlUsername, MessageElementData.getCPtr(UrlCredentials), UrlCredentials, vectorstring.getCPtr(ServiceTypes), ServiceTypes, WrappedServiceSubscriptionFilter.getCPtr(Filter), Filter), true);
  }

  public WrappedServiceSubscriptionManagerDetails(String Name, ServiceSubscriptionManager_CONNECTION_METHOD Connection_method, vectorstring Urls, String UrlUsername, MessageElementData UrlCredentials, vectorstring ServiceTypes) {
    this(RobotRaconteurJavaJNI.new_WrappedServiceSubscriptionManagerDetails__SWIG_3(Name, Connection_method.swigValue(), vectorstring.getCPtr(Urls), Urls, UrlUsername, MessageElementData.getCPtr(UrlCredentials), UrlCredentials, vectorstring.getCPtr(ServiceTypes), ServiceTypes), true);
  }

  public WrappedServiceSubscriptionManagerDetails(String Name, ServiceSubscriptionManager_CONNECTION_METHOD Connection_method, vectorstring Urls, String UrlUsername, MessageElementData UrlCredentials) {
    this(RobotRaconteurJavaJNI.new_WrappedServiceSubscriptionManagerDetails__SWIG_4(Name, Connection_method.swigValue(), vectorstring.getCPtr(Urls), Urls, UrlUsername, MessageElementData.getCPtr(UrlCredentials), UrlCredentials), true);
  }

  public WrappedServiceSubscriptionManagerDetails(String Name, ServiceSubscriptionManager_CONNECTION_METHOD Connection_method, vectorstring Urls, String UrlUsername) {
    this(RobotRaconteurJavaJNI.new_WrappedServiceSubscriptionManagerDetails__SWIG_5(Name, Connection_method.swigValue(), vectorstring.getCPtr(Urls), Urls, UrlUsername), true);
  }

  public WrappedServiceSubscriptionManagerDetails(String Name, ServiceSubscriptionManager_CONNECTION_METHOD Connection_method, vectorstring Urls) {
    this(RobotRaconteurJavaJNI.new_WrappedServiceSubscriptionManagerDetails__SWIG_6(Name, Connection_method.swigValue(), vectorstring.getCPtr(Urls), Urls), true);
  }

  public WrappedServiceSubscriptionManagerDetails(String Name, ServiceSubscriptionManager_CONNECTION_METHOD Connection_method) {
    this(RobotRaconteurJavaJNI.new_WrappedServiceSubscriptionManagerDetails__SWIG_7(Name, Connection_method.swigValue()), true);
  }

  public WrappedServiceSubscriptionManagerDetails(String Name) {
    this(RobotRaconteurJavaJNI.new_WrappedServiceSubscriptionManagerDetails__SWIG_8(Name), true);
  }

}
