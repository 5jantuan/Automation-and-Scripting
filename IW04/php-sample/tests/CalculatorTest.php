<?php
use PHPUnit\Framework\TestCase;
use App\Calculator;

final class CalculatorTest extends TestCase {
    public function testAdd() {
        $c = new Calculator();
        $this->assertEquals(4, $c->add(2,2));
    }
}
