//This file is automatically generated. DO NOT EDIT!
package com.robotraconteur.testing.TestService1;
import java.util.*;
import com.robotraconteur.*;
public interface async_sub1
{
    void async_get_d1(Action2<double[],RuntimeException> rr_handler, int rr_timeout);
    void async_set_d1(double[] value, Action1<RuntimeException> rr_handler, int rr_timeout);
    void async_get_d2(Action2<MultiDimArray,RuntimeException> rr_handler, int rr_timeout);
    void async_set_d2(MultiDimArray value, Action1<RuntimeException> rr_handler, int rr_timeout);
    void async_get_s_ind(Action2<String,RuntimeException> rr_handler, int rr_timeout);
    void async_set_s_ind(String value, Action1<RuntimeException> rr_handler, int rr_timeout);
    void async_get_i_ind(Action2<Integer,RuntimeException> rr_handler, int rr_timeout);
    void async_set_i_ind(int value, Action1<RuntimeException> rr_handler, int rr_timeout);
    void async_get_o2_1(Action2<sub2,RuntimeException> handler, int timeout);
    void async_get_o2_2(int ind, Action2<sub2,RuntimeException> handler, int timeout);
    void async_get_o2_3(String ind, Action2<sub2,RuntimeException> handler, int timeout);
}

