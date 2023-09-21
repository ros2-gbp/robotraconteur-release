// This file is automatically generated. DO NOT EDIT!

#include <RobotRaconteur.h>

#pragma once

#pragma warning(push)
#pragma warning(disable : 4996)
#include <boost/signals2.hpp>

namespace RobotRaconteurServiceIndex
{

class NodeInfo;
class ServiceInfo;
class ServiceIndex;

class NodeInfo : public RobotRaconteur::RRStructure
{
  public:
    std::string NodeName;
    RR_INTRUSIVE_PTR<RobotRaconteur::RRArray<uint8_t> > NodeID;
    RR_INTRUSIVE_PTR<RobotRaconteur::RRMap<int32_t, RobotRaconteur::RRArray<char> > > ServiceIndexConnectionURL;

    RR_OVIRTUAL std::string RRType() RR_OVERRIDE { return "RobotRaconteurServiceIndex.NodeInfo"; }
};

class ServiceInfo : public RobotRaconteur::RRStructure
{
  public:
    std::string Name;
    std::string RootObjectType;
    RR_INTRUSIVE_PTR<RobotRaconteur::RRMap<int32_t, RobotRaconteur::RRArray<char> > > RootObjectImplements;
    RR_INTRUSIVE_PTR<RobotRaconteur::RRMap<int32_t, RobotRaconteur::RRArray<char> > > ConnectionURL;
    RR_INTRUSIVE_PTR<RobotRaconteur::RRMap<std::string, RobotRaconteur::RRValue> > Attributes;

    RR_OVIRTUAL std::string RRType() RR_OVERRIDE { return "RobotRaconteurServiceIndex.ServiceInfo"; }
};

class ServiceIndex : public virtual RobotRaconteur::RRObject
{
  public:
    virtual RR_INTRUSIVE_PTR<RobotRaconteur::RRMap<int32_t, ServiceInfo> > GetLocalNodeServices() = 0;

    virtual RR_INTRUSIVE_PTR<RobotRaconteur::RRMap<int32_t, NodeInfo> > GetRoutedNodes() = 0;

    virtual RR_INTRUSIVE_PTR<RobotRaconteur::RRMap<int32_t, NodeInfo> > GetDetectedNodes() = 0;

    virtual boost::signals2::signal<void()>& get_LocalNodeServicesChanged() = 0;

    RR_OVIRTUAL std::string RRType() RR_OVERRIDE { return "RobotRaconteurServiceIndex.ServiceIndex"; }
};

} // namespace RobotRaconteurServiceIndex

#pragma warning(pop)