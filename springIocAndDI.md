---
title: Spring的IoC和DI
date: 2020-06-21 13:29:29
tags: Spring
categories: Java
cover: /img/myphotos/spring.png
---
## Bean

在Web开发或者软件开发中，我们通常把一些需要复用的代码抽取出来，写成一个个工具类，或者说组件。我们把这些组件称为JavaBean、Bean(Bean英文原意为豌豆)。Spring框架的主要功能就是对这些组件(Beans)的创建和依赖关系，以IoC和DI的方式进行管理。

我们可以把Spring看作是一个大型工厂，这个工厂的作用就是生产和管理Spring容器中的Bean。

## Spring核心容器

Spring对Bean的生产管理功能是通过其核心容器实现的，Spring有两种核心的IoC容器：

1. **BeanFactory：**
    BeanFactoty由org.springframework.beans.facytory.BeanFactory接口定义。由于这个核心容器在实际开发中并不多用，所以不过多介绍，也不介绍其实现类。

2. **ApplicationContext：**
    ApplicationContext是BeanFactory的子接口，由org.springframework.context.ApplicationContext接口定义。不仅支持BeanFactory的所有功能，还添加了对国际化、资源访问等方面的支持。

下面介绍ApplicationContext的实现类：

1. **通过ClassPathXmlApplicationContext创建Spring容器：**
    ClassPathXmlApplicationContext会从**项目的类路径**寻找指定的XML配置文件并装载，完成Spring容器的实例化工作。

2. **通过FileSystemXmlApplicationContext创建Spring容器：**
    FileSystemXmlApplicationContext会从**操作系统文件目录路径**寻找指定的XML配置文件并装载，完成Spring容器的实例化工作。

实例化Spring容器的语句：

``` java
/*
    一般不使用FileSystemXmlApplicationContext类来实例化Spring容器
*/
ApplicationContext applicationContext = new ClassPathXmlApplicationContext(String XMLPath);
```

**值得一提的是，在普通的Java项目中，我们要使用Spring容器，就要自己把它实例化出来。不过在Web项目中，我们可以把这项工作交给Web服务器来完成，只需在Web项目的配置文件web.xml中添加下面几行语句：**

``` xml
<!-- 指定Spring配置文件的位置，多个配置文件以逗号分隔 -->
<context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath:applicationContext.xml</param-value>
<!-- Spring配置文件一般以applicationContext命名，直接放在项目的src目录下 -->
</context-param>
<!-- 指定Web服务器以ContextLoaderListener的方式启动Spring容器 -->
<listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
```

## 配置Bean

要让Spring对Bean进行管理，就要在Spring的配置文件中对Bean进行配置。

Spring的配置文件支持XML和Properties两种格式的文件，一般使用XML文件。

在Spring中，XML配置文件的根元素是`<beans>`，`<beans>`中包含多个`<bean>`子元素，每个`<bean>`元素对应了一个Bean，并描述了该Bean如何被装配到Spring容器中。

`<bean>`元素的常用属性及子元素：

![bean元素的常用属性及子元素](/img/myphotos/spring-bean.png)

通常在XML文件中只需配置Bean的id和class属性就可以了：

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:aop="http://www.springframework.org/schema/aop"
	xmlns:tx="http://www.springframework.org/schema/tx"
	xmlns:context="http://www.springframework.org/schema/context"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
            http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/tx 
            http://www.springframework.org/schema/tx/spring-tx.xsd
            http://www.springframework.org/schema/context 
            http://www.springframework.org/schema/context/spring-context.xsd
            http://www.springframework.org/schema/aop 
            http://www.springframework.org/schema/aop/spring-aop.xsd">
    <bean id="Bean的唯一标识名称" class="Bean的实际类路径" /> 
</beans>
```

+ Spring的XML配置文件约束比较多，手写浪费时间也容易出错，可以直接复制相同Spring版本的配置文件约束就好了。或者打开Spring解压缩文件，在doc目录下，找到spring-framework-reference文件夹打开，然后找到html文件夹打开，最后找到index.html文件。用浏览器打开index.html文件，在Overview of SpringFramework下的Configuration metadata小节中就有配置文件的约束信息，如果没有就在这个文件中多找找。

## 获取Bean

我们在配置好Bean后，可以从Spring容器这个工厂中获取到Bean的实例化对象，通过下面两种方法：

1. Object getBean(String BeanID)：需要将返回结果强制转型。

2. `<T>` T getBean(Class`<T>` BeanType)：泛型方法，不需要强制转型。

例子：

``` java
//通过Spring容器的实例化对象获取Bean
ApplicationContext applicationContext = new ClassPathXmlApplicationContext(String XMLPath);
Bean bean = (Bean) applicationContext.getBean("BeanID"); //强制转换为跟Bean的类型一样
```

## IoC和DI

IoC，全称Inversion of Control，意思是控制反转。DI，全称是Dependency Injection，意思是依赖注入。

**这两个概念的含义相同，不过是从两个不同的角度来描述同一个概念。**

在以前的方式中，当在某个Java类中需要使用另一个Java类的对象时，我们是要在这个类的代码中，自己`new`一个被调用的对象出来。

在使用Spring后，对象的实例不再由我们写的代码来创建，而是由Spring容器来创建。这样，Spring容器负责控制Bean之间的关系，而不是我们写的程序代码直接控制。比如上面介绍的Spring中的Bean，我们并没有直接`new`出Bean的实例化对象出来，而是通过Spring容器来进行创建和获取。

**所以，站在程序员的角度来看，控制权发生了反转，这就是Spring的控制反转，IoC。**

**站在Spring的角度来看，Spring容器负责实例化程序代码中需要用到或者说依赖的对象，并注入到代码的成员变量(属性)中，这就是Spring的依赖注入，DI。**

**依赖注入的作用就是在Spring容器中实例化一个对象(Bean、组件)时，可以动态地将其所依赖的对象注入其中，即为类的属性(成员变量)注入值。**

Spring容器进行依赖注入的方式有两种：

1. 通过属性的setter()方法注入。

2. 通过类的构造方法注入。

## Bean的装配方式

Bean中的依赖对象，可以通过Spring的依赖注入方式进行装配，主要有基于XML的装配，基于注解(Annotation)的装配和自动装配三种方式。

### 基于XML装配

基于XML的装配方式有两种：设值注入和构造注入，也就是依赖注入的两种方式。

下面重点只讲设值注入的方式。

#### 设值注入

在Spring实例化Bean的过程中，Spring会先调用Bean的默认无参构造方法来实例化Bean对象，然后通过**反射**的方式调用setter()方法注入属性值。

因此设值注入必须满足以下两点要求：

+ Bean类必须提供一个默认的无参构造方法。

+ Bean类必须为需要注入值的属性提供相应的setter()方法。

然后在Spring配置文件中，配置Bean，并通过`<bean>`元素的子元素`<property>`来为属性注入值。

例子：

``` xml
<!-- 设值注入 -->
<bean id="beanname" class="beanclasspath">
    <!-- 注入基本数据类型的值 -->
    <property name="属性名" value="属性值"></property>
    <!-- 可以注入另一个Bean -->
    <property name="属性名" ref="另一个Bean的id"></property>
    <!-- 可以注入List类型的属性 -->
    <property name="属性名">
        <list>
            <value>"属性值1"</value>
            <value>"属性值2"</value>
        </list>
    </property>
</bean>
```

### 基于注解装配

如果基于XML对Bean进行装配，那么随着Bean的增多，Spring的配置文件会越来越臃肿，对后续的系统维护和升级工作带来一定的困难。为此，Spring提供了对**注解技术**的全面支持。

Spring中定义了一系列的注解：

![Spring的注解](/img/myphotos/spring-annotation.png)

在Bean类上添加相应层的注解，接着在依赖对象上添加@Autowired或@Resource注解，然后在Spring配置文件中完成对相应的Bean的配置，不用设置`<property>`，就可以实现依赖注入了。

例子：

``` java
import org.springframework.beans.factory.annotation.Autowired; //导入注解类
import org.springframework.stereotype.Service;

import com.java.util.AnotherBean;

@Service
public class ServiceBeanImpl{

    ...

    @Autowired
    private AnotherBean bean;

    ...
}

```

``` xml
<bean id="AnotherBean" class="com.java.util.AnotherBean" />
<bean id="ServiceBeanImpl" class="com.java.util.ServiceBeanImpl" /> 
```

不过这样还是要在配置文件中配置相应的Bean，为此，Spring注解提供了一种高效的注解配置方式，也就是对包路径下的所有Bean文件进行注解的扫描，只需在配置文件中添加一条语句：

``` xml
<!-- 使用context命名空间，通知Spring容器扫描指定包下的所有Bean类，进行注解解析 -->
<context:component-scan base-package="指定的包路径" />
```

+ 注意，Spring4.0以上的版本，使用注解扫描时，还需要额外在项目中导入Spring AOP模块的spring-aop-版本号.RELEASE.jar包。

这样在配置文件中就不用配置Bean了，一句话就搞定了。而且基于注解的装配方式还有一个好处，就是不用为属性写setter()方法。

### 自动装配

自动装配就是在不用注解的方式下，通过`<bean>`元素的autowire属性来进行自动装配。

![Bean的自动装配](/img/myphotos/spring_bean_autowire.png)

## 总结

要理解好IoC和DI的概念，掌握DI的方法和步骤。一般来说，Bean中的基本数据类型的属性通过setter()方法注入，要引用不同层的Bean的话就通过注解注入。

