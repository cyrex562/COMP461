<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="stripes" uri="http://stripes.sourceforge.net/stripes.tld" %>

<stripes:layout-definition>
    <html>
    <head>
        <title>Default Layout</title>
        <script type="text/javascript" src="js/jquery-1.11.1.js"></script>
        <script type="text/javascript" src="js/bootstrap.js"></script>
        <link rel="stylesheet" type="text/css" href="css/bootstrap.css"/>
        <link rel="stylesheet" type="text/css" href=css/bootstrap-theme.css"/>
        <link rel="stylesheet" type="text/css" xhref="css/styles.css"/>

        <stripes:layout-component name="html_head"/>
    </head>
    <body>
    <stripes:layout-component name="header">
        <jsp:include page="_header.jsp"/>
    </stripes:layout-component>

    <div class="page_content">
        <stripes:layout-component name="content"/>
    </div>

    <stripes:layout-component name="footer">
        <jsp:include page="_footer.jsp"/>
    </stripes:layout-component>
    </body>
    </html>
</stripes:layout-definition>
