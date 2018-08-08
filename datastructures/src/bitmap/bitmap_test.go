package bitmap

import (
	"reflect"
	"testing"
)

func TestAdd(t *testing.T) {
	var m BitMap
	m.Add(0)
	assertEqual(t, m, BitMap{[]uint64{1}})
	m.Add(63)
	assertEqual(t, m, BitMap{[]uint64{9223372036854775809}}) // 2^63+1

	var m2 BitMap
	m2.Add(128 + 10)
	assertEqual(t, m2, BitMap{[]uint64{0, 0, 1024}})
}

func TestDiscard(t *testing.T) {
	var m BitMap
	m.Discard(0)
	assertEqual(t, m, BitMap{})

	m.Add(0)
	m.Discard(64)
	assertEqual(t, m, BitMap{[]uint64{1}})
	m.Discard(0)
	assertEqual(t, m, BitMap{[]uint64{0}})

	m.Add(10)
	m.Discard(10)
	assertEqual(t, m, BitMap{[]uint64{0}})
	m.Add(128 + 10)
	m.Discard(128 + 10)
	assertEqual(t, m, BitMap{[]uint64{0, 0, 0}})
}

func TestContain(t *testing.T) {
	var m BitMap
	assert(t, !m.Contain(0))
	m.Add(0)
	assert(t, m.Contain(0))
	assert(t, !m.Contain(128+10))
	m.Add(128 + 10)
	assert(t, m.Contain(128+10))
}

func TestUnion(t *testing.T) {
	var m BitMap
	var m2 BitMap
	m2.Add(10)
	m.Union(m2)
	assertEqual(t, m, BitMap{[]uint64{1024}})

	m.Clear()
	m2.Clear()
	m.Add(10)
	m2.Add(20)
	m.Union(m2)
	assertEqual(t, m, BitMap{[]uint64{1049600}})

	m.Clear()
	m2.Clear()
	m2.Add(128 + 10)
	m.Union(m2)
	assertEqual(t, m, BitMap{[]uint64{0, 0, 1024}})
}

func TestIntersection(t *testing.T) {
	var m BitMap
	var m2 BitMap
	m2.Add(10)
	m.Intersection(m)
	assertEqual(t, m, BitMap{})

	m.Clear()
	m2.Clear()
	m.Add(20)
	m2.Add(10)
	m.Intersection(m2)
	assertEqual(t, m, BitMap{})

	m.Clear()
	m2.Clear()
	m.Add(20)
	m2.Add(20)
	m.Intersection(m2)
	assertEqual(t, m, BitMap{[]uint64{1048576}})

	m.Clear()
	m2.Clear()
	m.Add(20)
	m2.Add(20)
	m2.Add(128 + 10)
	m.Intersection(m2)
	assertEqual(t, m, BitMap{[]uint64{1048576}})

}

func TestDifference(t *testing.T) {
	var m BitMap
	var m2 BitMap
	m2.Add(10)
	m.Difference(m2)
	assertEqual(t, m, BitMap{})

	m.Add(10)
	m.Difference(m2)
	assertEqual(t, m, BitMap{})

	m.Add(10)
	m.Add(20)
	m.Difference(m2)
	assertEqual(t, m, BitMap{[]uint64{1048576}})

	m.Clear()
	m.Add(10)
	m.Add(20)
	m.Add(128 + 10)
	m.Difference(m2)
	assertEqual(t, m, BitMap{[]uint64{1048576, 0, 1024}})

	m.Clear()
	m2.Clear()
	m.Add(10)
	m2.Add(10)
	m2.Add(128 + 10)
	m.Difference(m2)
	assertEqual(t, m, BitMap{})
}

func TestIsEmpty(t *testing.T) {
	var m BitMap
	assert(t, m.IsEmpty())
	m.words = []uint64{0}
	assert(t, m.IsEmpty())
	m.Add(0)
	assert(t, !m.IsEmpty())
}

func TestClone(t *testing.T) {
	var m BitMap
	m2 := m.Clone()
	assertEqual(t, m2, BitMap{})

	m.Add(10)
	m2 = m.Clone()
	assertEqual(t, m2, BitMap{[]uint64{1024}})
	m.Add(138)
	m2 = m.Clone()
	assertEqual(t, m2, BitMap{[]uint64{1024, 0, 1024}})

}

func assertEqual(t *testing.T, m1, m2 BitMap) {
	if !reflect.DeepEqual(m1, m2) {
		t.Errorf("NotEqual: %+v, %+v", m1, m2)
	}
}

func assert(t *testing.T, b bool) {
	if !b {
		t.Errorf("False: %+v", b)
	}
}
