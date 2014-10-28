<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes.tld" %>
<stripes:layout-render name="layout.jsp" pageTitle="E-Commerce Site!:Login">
    <stripes:layout-component name="content">
        <h2>My Account</h2>

        <div class="container-fluid">
            <div class="row">
                <div class="col-xs-2">
                    <div style="position: absolute;">
                        <div class="btn-group-vertical">
                            <a class="btn btn-default" href="#account_summary">Summary</a>
                            <a class="btn btn-default" href="#account_orders">Orders</a>
                            <a class="btn btn-default" href="#account_information">Customer Information</a>
                        </div>
                    </div>
                </div>
                <div class="col-xs-10">
                    <div id="account_summary">
                        <legend>Account Summary</legend>
                    </div>
                    <div id="account_orders">
                        <legend>Order History</legend>

                    </div>
                    <div id="account_information">
                        <legend>Customer Information</legend>
                    </div>
                </div>
            </div>
        </div>
    </stripes:layout-component>
</stripes:layout-render>