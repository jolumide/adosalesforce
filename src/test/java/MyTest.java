import com.microsoft.demo.Demo;
import org.junit.Test;
//this is a test
public class MyTest {
    @Test
    public void test_method_1() {
        Demo d = new Demo();
        d.DoSomething(true);
    }

    @Test
    public void test_method_2() {
    }
}
